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
            "labels",
            ArrayType(
                StructType(
                    [
                        StructField("label_start_pos", IntegerType(), False),
                        StructField("label_end_pos", IntegerType(), False),
                        StructField("label_type", StringType(), False),
                    ]
                ),
                False,
            ),
            False,
        ),
    ]
)
