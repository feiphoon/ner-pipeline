from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
)


SYNTHESISED_ANNOTATIONS_INPUT_SCHEMA = StructType(
    [
        StructField("data", StringType(), False),
        StructField("id", StringType(), False),
        StructField("pmid", StringType(), False),
        StructField(
            "label", ArrayType(ArrayType(StringType(), True), True), False
        ),
        StructField("scientific_name", StringType(), False),
        StructField("scientific_name_id", StringType(), False),
        StructField("scientific_name_type", StringType(), False),
    ]
)


NER_ANNOTATIONS_OUTPUT_SCHEMA = StructType(
    [
        StructField("data", StringType(), False),
        StructField("id", StringType(), False),
        StructField("pmid", StringType(), False),
        StructField("entities", ArrayType(ArrayType(StringType(), True), True), False),
        StructField("scientific_name", StringType(), False),
        StructField("scientific_name_id", StringType(), False),
        StructField("scientific_name_type", StringType(), False),
    ]
)
