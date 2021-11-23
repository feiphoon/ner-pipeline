from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    ArrayType,
)


ANNOTATED_ABSTRACTS_INPUT_SCHEMA = StructType(
    [
        StructField("data", StringType(), True),
        StructField("id", StringType(), True),
        StructField("pmid", StringType(), True),
        StructField(
            "label",
            ArrayType(
                StringType(),
                False,
            ),
            False,
        ),
    ]
)
