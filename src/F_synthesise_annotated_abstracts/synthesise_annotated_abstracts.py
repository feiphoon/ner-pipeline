from pathlib import Path

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame

from src.helpers.train_val_test_split import TrainValTestSplit, check_valid_split
from src.F_synthesise_annotated_abstracts.schemas import (
    ANNOTATED_ABSTRACTS_INPUT_SCHEMA,
)


#  Monkeypatch in case I don't use Spark 3.0
def transform(self, f):
    return f(self)


DataFrame.transform = transform


def synthesise_annotated_abstracts(
    spark: SparkSession,
    run_input_filepath: Path,
    name_mappings_filepath: Path,
    run_output_filepath: Path,
    train_val_test_split: TrainValTestSplit,
    split_subset_type: str = "train",
    seed: int = 42,
) -> None:
    check_valid_split(train_val_test_split)

    name_mappings_df: DataFrame = spark.read.option(
        "basePath", f"{name_mappings_filepath}"
    ).load(f"{name_mappings_filepath}/scientific_name_type=*/")

    name_mappings_df = name_mappings_df.transform(filter_out_empty_name_mappings)

    print(name_mappings_df.show(truncate=False))

    annotated_abstracts_df: DataFrame = spark.read.json(
        str(Path(f"{run_input_filepath}/{split_subset_type}/"))
    )

    # print(annotated_abstracts_df.show(truncate=False))

    # if split_subset_type == "train":


def filter_out_empty_name_mappings(df: DataFrame) -> DataFrame:
    """
    This is a hack as I have a bug in the MPNS pipeline,
    where if a name can't be mapped to anything, it shows up
    as a non_scientific_name_count of 1, but 0 on the common
    and pharmaceutical name counts. I'm just going to filter
    the name mappings on this.
    """
    return df.filter(
        (f.col("common_name_count") != 0) & (f.col("pharmaceutical_name_count") != 0)
    )
