from pyspark.sql.types import StructType, StructField, StringType, ArrayType


INPUT_SCHEMA = StructType(
    [
        StructField("pmid", StringType(), False),
        StructField("doi", ArrayType(StringType(), True), True),
        StructField("language", ArrayType(StringType(), True), True),
        StructField("title", StringType(), False),
        StructField("abstract", StringType(), False),
        StructField("date_completed", StringType(), True),
        StructField("date_revised", StringType(), True),
    ]
)


OUTPUT_SCHEMA = StructType(
    [
        StructField("pmid", StringType(), False),
        StructField("text", StringType(), False),
    ]
)
