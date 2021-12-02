from pathlib import Path

from pyspark.sql import SparkSession, functions as f
from pyspark.sql.dataframe import DataFrame

# from pyspark.sql.types import (
#     StructType,
#     StructField,
#     IntegerType,
#     ArrayType,
#     StringType,
# )

from src.G_prepare_synthetic_annotations_for_ner.schemas import (
    SYNTHESISED_ABSTRACTS_INPUT_SCHEMA,
    NER_ABSTRACTS_OUTPUT_SCHEMA,
)


#  Monkeypatch in case I don't use Spark 3.0
def transform(self, f):
    return f(self)


DataFrame.transform = transform


def prepare_synthesised_abstracts_for_ner(
    spark: SparkSession,
    run_input_filepath: Path,
    run_output_filepath: Path,
    sample_run: bool = True,
) -> None:
    pass


prepare_synthesised_abstracts_for_ner(
    spark=SparkSession,
    run_input_filepath=Path(),
    run_output_filepath=Path(),
    sample_run=True,
)
