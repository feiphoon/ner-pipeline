from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    IntegerType,
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


MPNS_NAME_MAPPINGS_V5_SCHEMA = StructType(
    [
        StructField("mapping_id", IntegerType(), False),
        StructField("scientific_name_id", StringType(), False),
        StructField("scientific_name", StringType(), False),
        StructField("scientific_name_type", StringType(), False),
        StructField("scientific_name_length", IntegerType(), False),
        StructField(
            "common_names",
            ArrayType(
                StructType(
                    [
                        StructField("non_scientific_name", StringType(), False),
                        StructField("non_scientific_name_length", IntegerType(), False),
                        StructField("non_scientific_name_id", StringType(), False),
                    ]
                ),
                True,
            ),
            True,
        ),
        StructField(
            "pharmaceutical_names",
            ArrayType(
                StructType(
                    [
                        StructField("non_scientific_name", StringType(), False),
                        StructField("non_scientific_name_length", IntegerType(), False),
                        StructField("non_scientific_name_id", StringType(), False),
                    ]
                ),
                True,
            ),
            True,
        ),
        StructField("non_scientific_name_count", IntegerType(), False),
        StructField("common_name_count", IntegerType(), False),
        StructField("pharmaceutical_name_count", IntegerType(), False),
    ]
)
