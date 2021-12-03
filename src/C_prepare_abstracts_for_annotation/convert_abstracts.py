from pathlib import Path
import re

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StringType

from src.C_prepare_abstracts_for_annotation.schemas import INPUT_SCHEMA, OUTPUT_SCHEMA


def convert_abstracts(
    spark: SparkSession, run_input_filepath: Path, run_output_filepath: Path
) -> None:
    run_input_filepath_without_metadata: Path = Path(f"{run_input_filepath}/*/[0-9]*")

    df: DataFrame = spark.read.json(
        str(run_input_filepath_without_metadata),
        schema=INPUT_SCHEMA,
    )

    df: DataFrame = (
        df.select("pmid", "title", "abstract")
        .withColumn("text", f.concat_ws(" ", "title", "abstract"))
        .withColumn("text", strip_html_udf(f.col("text")))
        .drop("title", "abstract")
        .drop_duplicates()
    )

    # Repartition to ballpark of 5 parquet files for real data
    df.coalesce(1).write.format("json").mode("overwrite").option(
        "schema", OUTPUT_SCHEMA
    ).save(str(run_output_filepath))


def strip_html(text: str) -> str:
    pattern = re.compile(r"<.*?>")
    return pattern.sub("", text)


strip_html_udf = f.udf(strip_html, StringType())
