from pathlib import Path

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame

from schemas import INPUT_SCHEMA, OUTPUT_SCHEMA


def prepare_abstracts_for_annotation(
    spark, run_input_filepath: Path, run_output_filepath: Path
) -> None:
    run_input_filepath_without_metadata: Path = Path(f"{run_input_filepath}/*/[0-9]*")

    df: DataFrame = spark.read.json(
        run_input_filepath_without_metadata,
        schema=INPUT_SCHEMA,
    )

    df: DataFrame = (
        df.select("pmid", "title", "abstract")
        .withColumn("text", f.concat_ws(" ", "title", "abstract"))
        .drop("title", "abstract")
    )

    # Repartition to ballpark of 5 parquet files for real data
    df.coalesce(1).write.format("json").mode("overwrite").option(
        "schema", OUTPUT_SCHEMA
    ).save(run_output_filepath)


# def prepare_abstracts_for_annotation(
#     run_input_filepath: Path, run_output_filepath: Path
# ) -> None:
#     # Prepare the output filepath  - there will only be one
#     run_output_filepath_complete: Path = Path(f"{run_output_filepath}/")
#     run_output_filepath_complete.mkdir(parents=True, exist_ok=True)

#     input_folder_paths: List = get_directories(run_input_filepath)

#     # Per query folder, e.g. data/raw/pubmed_abstracts/2021-10-22-15-42-10/chia/
#     for _input_folder in input_folder_paths:

#         # Get all available file names in the input folder,
#         # Exclude the metadata file.
#         input_filepaths = [
#             file for file in get_files(_input_folder) if "metadata" not in file.name
#         ]

#         # Open every file in this query folder
#         for _input_file in input_filepaths:

#             # Create a new
#             with _input_file.open("r", encoding="utf-8") as f:
#                 result = json.load(f)

#                 result[]
