from pathlib import Path
from functools import reduce

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
    seed: int = 42,
) -> None:
    check_valid_split(train_val_test_split)

    name_mappings_df: DataFrame = spark.read.option(
        "basePath", f"{name_mappings_filepath}"
    ).load(f"{name_mappings_filepath}/scientific_name_type=*/")

    name_mappings_df = name_mappings_df.transform(filter_out_empty_name_mappings)

    # NOTE: This is perfect that this loads only train. It's the name mappings
    # which need to be split between train and val.
    annotated_abstracts_df: DataFrame = spark.read.json(
        str(Path(f"{run_input_filepath}/train/")),
        schema=ANNOTATED_ABSTRACTS_INPUT_SCHEMA,
    )

    annotated_abstracts_df = annotated_abstracts_df.withColumn(
        "entities_count", f.size(f.col("label"))
    )

    # print(annotated_abstracts_df.show(2))

    max_entities_in_annotated_abstracts: int = annotated_abstracts_df.agg(
        {"entities_count": "max"}
    ).collect()[0][0]

    # print(max_entities_in_annotated_abstracts)

    name_mappings_df_with_min_non_scientific_names: DataFrame = name_mappings_df.filter(
        f.col("non_scientific_name_count") >= max_entities_in_annotated_abstracts
    )

    stratified_name_mappings_df: DataFrame = (
        name_mappings_df_with_min_non_scientific_names.transform(
            lambda df: stratify_name_mappings(df, seed)
        )
    )

    print(stratified_name_mappings_df.count())

    # TODO: Do the stratification of name mappings here with the provided TrainValTestSplit value.


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


def perform_deterministic_shuffle(df: DataFrame, seed: int) -> DataFrame:
    """
    Hacky method of doing a shuffle with deterministic results.
    """
    return (
        df.orderBy(f.col("mapping_id").asc())
        .withColumn("order", f.rand(seed=seed))
        .orderBy(f.col("order").asc())
        .drop("order")
    )


def stratify_name_mappings(df: DataFrame, seed: int) -> DataFrame:
    """
    We find out which group of name mappings has the lowest representation
    in the name mappings resulting after a filter for minimum entity counts.
    We perform a deterministic shuffle (for reproducibility) and we grab enough
    items of each so that we have as many of each group as possible while
    maintaining equal representation.
    """
    # Slice up our dataframes into the three types to be stratified and perform
    # a deterministic shuffle so that this processing is reproducible.
    name_mappings_synonym_df: DataFrame = df.filter(
        f.col("scientific_name_type") == "synonym"
    ).transform(lambda df: perform_deterministic_shuffle(df, seed))

    name_mappings_sci_cited_medicinal_df: DataFrame = df.filter(
        f.col("scientific_name_type") == "sci_cited_medicinal"
    ).transform(lambda df: perform_deterministic_shuffle(df, seed))

    name_mappings_plant_df: DataFrame = df.filter(
        f.col("scientific_name_type") == "plant"
    ).transform(lambda df: perform_deterministic_shuffle(df, seed))

    # Take counts of rows in all three dataframe slices.
    name_mappings_synonym_count: int = name_mappings_synonym_df.count()
    name_mappings_sci_cited_medicinal_count: int = (
        name_mappings_sci_cited_medicinal_df.count()
    )
    name_mappings_plant_count: int = name_mappings_plant_df.count()

    # So I can work out what's the group with the lowest representation.
    name_mappings_min_count: int = min(
        [
            name_mappings_synonym_count,
            name_mappings_sci_cited_medicinal_count,
            name_mappings_plant_count,
        ]
    )

    # Grab the minimum count of items from each group.
    name_mappings_synonym_df = name_mappings_synonym_df.head(name_mappings_min_count)
    name_mappings_sci_cited_medicinal_df = name_mappings_sci_cited_medicinal_df.head(
        name_mappings_min_count
    )
    name_mappings_plant_df = name_mappings_plant_df.head(name_mappings_min_count)

    # Join all three name mapping groups for everything
    _dfs_to_union: list = [
        name_mappings_synonym_df,
        name_mappings_sci_cited_medicinal_df,
        name_mappings_plant_df,
    ]

    return reduce(DataFrame.union, _dfs_to_union)
