from pathlib import Path
from glob import glob
from zipfile import ZipFile

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame

from dataclasses import dataclass


@dataclass
class TrainValTestSplit:
    train: float
    val: float
    test: float


class InvalidSplitError(Exception):
    pass


def split_annotated_abstracts(
    spark: SparkSession,
    run_input_filepath: Path,
    run_output_filepath: Path,
    train_val_test_split: TrainValTestSplit,
    seed: int = 42,
    annotator: str = "admin",
) -> None:
    check_valid_split(train_val_test_split)

    # Extract the contents of the donloaded zip
    run_input_filepath_glob = glob(f"../../{run_input_filepath}/")
    run_input_filepath_zip_glob = glob(f"{run_input_filepath_glob[0]}/*.zip")

    with ZipFile(run_input_filepath_zip_glob[0], "r") as zip_f:
        zip_f.extractall(run_input_filepath_glob[0])

    # Spark read has glob support built in, so we switch to that.
    # We assume that there will be a master annotation file that has agreement from all parties.
    annotations_df: DataFrame = spark.read.json(
        str(Path(f"{run_input_filepath}/{annotator}.jsonl"))
    )

    # Perform splits
    train_and_val_split = train_val_test_split.train + train_val_test_split.val

    int_train_df, test_df = annotations_df.randomSplit(
        weights=[
            train_and_val_split,
            train_val_test_split.test,
        ],
        seed=seed,
    )

    train_df, val_df = int_train_df.randomSplit(
        weights=[
            train_val_test_split.train / train_and_val_split,
            train_val_test_split.val / train_and_val_split,
        ],
        seed=seed,
    )

    # Write dfs to files
    run_output_filepath.mkdir(parents=True, exist_ok=True)

    train_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(Path(f"{run_output_filepath}/train"))
    )

    val_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(Path(f"{run_output_filepath}/val"))
    )

    test_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(Path(f"{run_output_filepath}/test"))
    )


def check_valid_split(split_config: TrainValTestSplit) -> bool:
    if (split_config.train + split_config.val + split_config.test) != 1:
        raise InvalidSplitError("Split config must add up to 1.")
