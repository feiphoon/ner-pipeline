from pathlib import Path
from glob import glob
from zipfile import ZipFile

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.window import Window

from dataclasses import dataclass


@dataclass
class TrainTestSplit:
    train: float
    test: float


class InvalidSplitError(Exception):
    pass


def split_annotated_abstracts(
    spark: SparkSession,
    run_input_filepath: Path,
    run_output_filepath: Path,
    train_test_split: TrainTestSplit,
    seed: int = 42,
    annotator: str = "admin",
) -> None:
    check_valid_split(train_test_split)

    # Extract the contents of the downloaded zip
    run_input_filepath_glob = glob(f"../../{run_input_filepath}/")
    run_input_filepath_zip_glob = glob(f"{run_input_filepath_glob[0]}/*.zip")

    with ZipFile(run_input_filepath_zip_glob[0], "r") as zip_f:
        zip_f.extractall(run_input_filepath_glob[0])

    # Spark read has glob support built in, so we switch to that.
    # We assume that there will be a master annotation file that has agreement from all parties.
    annotations_df: DataFrame = spark.read.json(
        str(Path(f"{run_input_filepath}/{annotator}.jsonl"))
    )

    annotations_df = annotations_df.transform(
        lambda df: perform_deterministic_shuffle(df, seed)
    ).transform(lambda df: assign_train_flag(df, train_test_split.train))

    train_df: DataFrame = annotations_df.filter(f.col("is_train")).drop("is_train")
    test_df: DataFrame = annotations_df.filter(~f.col("is_train")).drop("is_train")

    # Write dfs to files
    run_output_filepath.mkdir(parents=True, exist_ok=True)

    train_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(Path(f"{run_output_filepath}/train"))
    )

    test_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(Path(f"{run_output_filepath}/test"))
    )


def check_valid_split(split_config: TrainTestSplit) -> bool:
    if (split_config.train + split_config.test) != 1:
        raise InvalidSplitError("Split config must add up to 1.")


def perform_deterministic_shuffle(df: DataFrame, seed: int) -> DataFrame:
    """
    Hacky method of doing a shuffle with deterministic results.
    Use the pmid metadata included with the abstracts as an anchor.
    """
    return (
        df.orderBy(f.col("pmid").asc())
        .withColumn("order", f.rand(seed=seed))
        .orderBy(f.col("order").asc())
    )


def assign_train_flag(df: DataFrame, train_split: float) -> DataFrame:
    total_rows: int = df.count()
    return (
        df.withColumn("id", f.row_number().over(Window.orderBy("order")))
        .withColumn("id_split", (f.col("id") / f.lit(total_rows)))
        .withColumn(
            "is_train",
            f.when(f.col("id_split") < f.lit(train_split), True).otherwise(False),
        )
        .drop("order", "id_split")
    )
