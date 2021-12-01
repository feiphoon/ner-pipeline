from pathlib import Path
from functools import reduce
from typing import List, Any, Tuple

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import (
    ArrayType,
    StringType,
    StructType,
    StructField,
    IntegerType,
)

from src.helpers.train_test_split import TrainTestSplit, check_valid_split
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
    train_test_split: TrainTestSplit,
    split_subset_type: str = "train",
    exclude_scientific_name_ids: List[str] = None,
    seed: int = 42,
) -> None:
    check_valid_split(train_test_split)

    name_mappings_df: DataFrame = spark.read.option(
        "basePath", f"{name_mappings_filepath}"
    ).load(f"{name_mappings_filepath}/scientific_name_type=*/")

    name_mappings_df = name_mappings_df.transform(
        filter_out_empty_name_mappings
    ).transform(
        lambda df: filter_out_plant_ids_from_name_mappings(
            df, exclude_scientific_name_ids
        )
    )

    annotated_abstracts_df: DataFrame = spark.read.json(
        str(Path(f"{run_input_filepath}/{split_subset_type}/")),
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

    # There may be an issue with not enough names from a certain label being present in the mapping.
    # So we produce a column in both dataframes to describe what entities need mapping, vs how many names
    # are available to be mapped. Then perform a cross-join, or a Cartesian product, and then extract only
    # the combinations eligible for mapping.
    annotated_abstracts_df: DataFrame = annotated_abstracts_df.withColumn(
        "ab_sci_com_pha", f.flatten(f.col("label"))
    ).withColumn(
        "ab_sci_com_pha", create_tuple_of_name_counts_udf(f.col("ab_sci_com_pha"))
    )

    stratified_name_mappings_df = stratified_name_mappings_df.withColumn(
        "nm_sci_com_pha",
        f.struct(
            f.lit(1).alias("sci"),
            f.col("common_name_count").cast(IntegerType()).alias("com"),
            f.col("pharmaceutical_name_count").cast(IntegerType()).alias("pha"),
        ),
    )

    monster_df = stratified_name_mappings_df.crossJoin(annotated_abstracts_df)

    # Check which rows are "mappable". This means that there's enough counts of every type of label
    # in each mapping, to match or exceed that found in the annotated abstracts.
    # So we want combinations where the name mappings can meet the composition of labelled entities.
    monster_df.withColumn(
        "mappable",
        f.when(f.col("nm_sci_com_pha") >= f.col("ab_sci_com_pha"), True).otherwise(
            False
        ),
    )

    # # Filter out the unmappable ones
    # mappable_combinations_df = monster_df.filter(f.col("mappable"))
    # # Filter out abstracts that don't have a scientific name - they must have at least one.
    # # TODO: Do this upstream, so this is not really a TODO for here.

    # Now for each name_mappings_df, we should run through all the abstracts
    # and replace the entities with new entities.
    # For each abstract, we want to replace the entities with a new set from name mappings.

    # abstracts_df = spark.read.json(
    #     "/Users/fei/projects/inm363-individual-project/ner-pipeline/data/sample_data/sample_annotated_abstract.json"
    # )

    # name_mappings_df = spark.read.json(
    #     "/Users/fei/projects/inm363-individual-project/ner-pipeline/data/sample_data/sample_name_mappings.json"
    # )


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


def filter_out_plant_ids_from_name_mappings(
    df: DataFrame, exclude_scientific_name_ids: List[str]
) -> DataFrame:
    if not exclude_scientific_name_ids:
        return df

    for _id in exclude_scientific_name_ids:
        df = df.filter(~f.col("scientific_name_id") == _id)
    return df


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
    maintaining EQUAL representation.
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


def create_tuple_of_name_counts(lst: List[Any]) -> Tuple[int]:
    """Scientific count is hardcoded to 1 - because scientific names will just be repeated."""
    alpha_lst = [el for el in lst if str(el).isalpha()]
    return tuple(
        list(
            map(
                str,
                [
                    alpha_lst.count("scientific"),
                    alpha_lst.count("common"),
                    alpha_lst.count("pharmaceutical"),
                ],
            )
        )
    )


create_tuple_of_name_counts_udf = f.udf(
    create_tuple_of_name_counts,
    StructType(
        [
            StructField("sci", IntegerType(), False),
            StructField("com", IntegerType(), False),
            StructField("pha", IntegerType(), False),
        ]
    ),
)
