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
            "new_common_entities", ArrayType(ArrayType(StringType(), True), True), False
        ),
        StructField(
            "new_scientific_entities",
            ArrayType(ArrayType(StringType(), True), True),
            False,
        ),
        StructField(
            "new_pharmaceutical_entities",
            ArrayType(ArrayType(StringType(), True), True),
            False,
        ),
        StructField("scientific_name", StringType(), False),
        StructField("scientific_name_id", StringType(), False),
        StructField("scientific_name_type", StringType(), False),
    ]
)


# SYNTHESISED_ANNOTATIONS_INPUT_SCHEMA = StructType(
#     [
#         # StructField(
#         #     "ab_com_pha",
#         #     StructType(
#         #         [
#         #             StructField("com", IntegerType(), True),
#         #             StructField("pha", IntegerType(), True),
#         #         ]
#         #     ),
#         #     True,
#         # ),
#         StructField("common_entities", ArrayType(StringType(), True), True),
#         # StructField("common_name_count", IntegerType(), True),
#         StructField(
#             "common_names",
#             ArrayType(
#                 StructType(
#                     [
#                         StructField("non_scientific_name", StringType(), True),
#                         StructField("non_scientific_name_id", StringType(), True),
#                         StructField("non_scientific_name_length", IntegerType(), True),
#                     ]
#                 ),
#                 True,
#             ),
#             True,
#         ),
#         StructField("data", StringType(), True),
#         StructField("id", StringType(), True),
#         StructField("label", ArrayType(ArrayType(StringType(), True), True), True),
#         StructField("mapping_id", IntegerType(), True),
#         StructField(
#             "new_common_entities", ArrayType(ArrayType(StringType(), True), True), True
#         ),
#         StructField(
#             "new_scientific_entities",
#             ArrayType(ArrayType(StringType(), True), True),
#             True,
#         ),
#         StructField(
#             "new_pharmaceutical_entities",
#             ArrayType(ArrayType(StringType(), True), True),
#             True,
#         ),
#         # StructField("non_scientific_name_count", IntegerType(), True),
#         StructField("pharmaceutical_entities", ArrayType(StringType(), True), True),
#         # StructField("pharmaceutical_name_count", IntegerType(), True),
#         StructField(
#             "pharmaceutical_names",
#             ArrayType(
#                 StructType(
#                     [
#                         StructField("non_scientific_name", StringType(), True),
#                         StructField("non_scientific_name_id", StringType(), True),
#                         StructField("non_scientific_name_length", IntegerType(), True),
#                     ]
#                 ),
#                 True,
#             ),
#             True,
#         ),
#         StructField("pmid", StringType(), True),
#         StructField("scientific_entities", ArrayType(StringType(), True), True),
#         StructField("scientific_name", StringType(), True),
#         StructField("scientific_name_id", StringType(), True),
#         # StructField("scientific_name_length", IntegerType(), True),
#         StructField("scientific_name_type", StringType(), True),
#     ]
# )


# root
#  |-- ab_com_pha: struct (nullable = True)
#  |    |-- com: long (nullable = True)
#  |    |-- pha: long (nullable = True)
#  |-- common_entities: array (nullable = True)
#  |    |-- element: string (containsNull = True)
#  |-- common_name_count: long (nullable = True)
#  |-- common_names: array (nullable = True)
#  |    |-- element: struct (containsNull = True)
#  |    |    |-- non_scientific_name: string (nullable = True)
#  |    |    |-- non_scientific_name_id: string (nullable = True)
#  |    |    |-- non_scientific_name_length: long (nullable = True)
#  |-- data: string (nullable = True)
#  |-- id: string (nullable = True)
#  |-- label: array (nullable = True)
#  |    |-- element: array (containsNull = True)
#  |    |    |-- element: string (containsNull = True)
#  |-- mapping_id: long (nullable = True)
#  |-- new_common_entities: array (nullable = True)
#  |    |-- element: array (containsNull = True)
#  |    |    |-- element: string (containsNull = True)
#  |-- new_scientific_entities: array (nullable = True)
#  |    |-- element: array (containsNull = True)
#  |    |    |-- element: string (containsNull = True)
#  |-- non_scientific_name_count: long (nullable = True)
#  |-- pharmaceutical_entities: array (nullable = True)
#  |    |-- element: string (containsNull = True)
#  |-- pharmaceutical_name_count: long (nullable = True)
#  |-- pharmaceutical_names: array (nullable = True)
#  |    |-- element: struct (containsNull = True)
#  |    |    |-- non_scientific_name: string (nullable = True)
#  |    |    |-- non_scientific_name_id: string (nullable = True)
#  |    |    |-- non_scientific_name_length: long (nullable = True)
#  |-- pmid: string (nullable = True)
#  |-- scientific_entities: array (nullable = True)
#  |    |-- element: string (containsNull = True)
#  |-- scientific_name: string (nullable = True)
#  |-- scientific_name_id: string (nullable = True)
#  |-- scientific_name_length: long (nullable = True)
#  |-- scientific_name_type: string (nullable = True)


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
