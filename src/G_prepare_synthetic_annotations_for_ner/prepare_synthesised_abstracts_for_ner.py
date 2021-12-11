from pathlib import Path

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame

from src.helpers.run import Run, get_last_run_timestamp

from src.G_prepare_synthetic_annotations_for_ner.schemas import (
    SYNTHESISED_ANNOTATIONS_INPUT_SCHEMA,
)


def prepare_synthesised_abstracts_for_ner(
    spark: SparkSession,
    run_input_filepath: Path,
    run_output_filepath: Path,
) -> None:

    synthesised_abstracts_df: DataFrame = spark.read.json(
        str(run_input_filepath), schema=SYNTHESISED_ANNOTATIONS_INPUT_SCHEMA
    )

    synthesised_abstracts_df: DataFrame = synthesised_abstracts_df.select(
        "pmid",
        "id",
        "data",
        "scientific_name_id",
        "scientific_name",
        "scientific_name_type",
        "label",
    )

    # print(synthesised_abstracts_df.show(5, truncate=False))
    # print(synthesised_abstracts_df.printSchema())

    # Aggregrate the new entities columns to replace the old labels column
    synthesised_abstracts_df: DataFrame = synthesised_abstracts_df.withColumnRenamed(
        "label", "entities"
    )

    # Then write cleaned_data
    run_output_filepath.mkdir(parents=True, exist_ok=True)

    synthesised_abstracts_df.coalesce(1).write.format("json").mode("overwrite").save(
        str(run_output_filepath)
    )


run = Run(last_run_timestamp=get_last_run_timestamp())
