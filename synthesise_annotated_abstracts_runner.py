from pathlib import Path
from pyspark.sql import SparkSession

from src.helpers.run import Run, get_last_run_timestamp
from src.helpers.train_test_split import TrainTestSplit

from src.F_synthesise_annotated_abstracts.prepare_annotated_abstracts_for_entity_replacement import (
    prepare_annotated_abstracts,
)

from F_synthesise_annotated_abstracts.entity_replacement import (
    perform_entity_replacement,
)


TRAIN_TEST_SPLIT = TrainTestSplit(0.5, 0.5)
SEED = 1

spark = SparkSession.builder.appName("run_ner_pipeline").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
run = Run(last_run_timestamp=get_last_run_timestamp())

# Sample run
split_annotated_abstracts_filepath: str = "data/processed/split_annotated_abstracts"
name_mappings_filepath: str = "data/reference/mpns_v8/mpns_name_mappings/v5-sample"
prepared_annotated_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/A_prepared/test"
)
prepare_annotated_abstracts(
    spark=spark,
    run_input_filepath=run.create_run_filepath(split_annotated_abstracts_filepath),
    name_mappings_filepath=Path(name_mappings_filepath),
    run_output_filepath=run.create_run_filepath(prepared_annotated_abstracts_filepath),
    train_test_split=TRAIN_TEST_SPLIT,
    split_subset_type="train",
    exclude_scientific_name_ids=["wcs516286", "wcsCmp708815"],
    seed=SEED,
)

prepared_annotated_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/A_prepared/test"
)

interim_scientific_names_replaced_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/B_scientific_replaced/test"
)
perform_entity_replacement(
    run_input_filepath=run.create_run_filepath(prepared_annotated_abstracts_filepath),
    run_output_filepath=run.create_run_filepath(
        interim_scientific_names_replaced_abstracts_filepath
    ),
    entity_type_to_replace="scientific",
    seed=SEED,
    sample_run=True,
)

interim_common_names_replaced_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/C_common_replaced/test"
)
perform_entity_replacement(
    run_input_filepath=run.create_run_filepath(
        interim_scientific_names_replaced_abstracts_filepath
    ),
    run_output_filepath=run.create_run_filepath(
        interim_common_names_replaced_abstracts_filepath
    ),
    entity_type_to_replace="common",
    seed=SEED,
)

interim_pharmaceutical_names_replaced_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts/D_pharmaceutical_replaced/test"
)
perform_entity_replacement(
    run_input_filepath=run.create_run_filepath(
        interim_common_names_replaced_abstracts_filepath
    ),
    run_output_filepath=run.create_run_filepath(
        interim_pharmaceutical_names_replaced_abstracts_filepath
    ),
    entity_type_to_replace="pharmaceutical",
    seed=SEED,
)

# Real data run
# split_annotated_abstracts_filepath: str = "data/processed/split_annotated_abstracts"
# name_mappings_filepath: str = "data/reference/mpns_v8/mpns_name_mappings/v5"
# prepared_annotated_abstracts_filepath: str = (
#     "data/processed/synthesised_annotated_abstracts/A_prepared"
# )
# prepare_annotated_abstracts(
#     spark=spark,
#     run_input_filepath=run.create_run_filepath(split_annotated_abstracts_filepath),
#     name_mappings_filepath=Path(name_mappings_filepath),
#     run_output_filepath=run.create_run_filepath(prepared_annotated_abstracts_filepath),
#     train_test_split=TRAIN_TEST_SPLIT,
#     split_subset_type="train",
#     exclude_scientific_name_ids=["wcs516286", "wcsCmp708815"],
#     seed=SEED,
# )

# prepared_annotated_abstracts_filepath: str = (
#     "data/processed/synthesised_annotated_abstracts/A_prepared"
# )

# interim_scientific_names_replaced_abstracts_filepath: str = (
#     "data/processed/synthesised_annotated_abstracts/B_scientific_replaced"
# )
# perform_entity_replacement(
#     run_input_filepath=run.create_run_filepath(prepared_annotated_abstracts_filepath),
#     run_output_filepath=run.create_run_filepath(
#         interim_scientific_names_replaced_abstracts_filepath
#     ),
#     entity_type_to_replace="scientific",
#     seed=SEED,
#     # sample_run=True,
# )

# interim_common_names_replaced_abstracts_filepath: str = (
#     "data/processed/synthesised_annotated_abstracts/C_common_replaced"
# )
# perform_entity_replacement(
#     run_input_filepath=run.create_run_filepath(
#         interim_scientific_names_replaced_abstracts_filepath
#     ),
#     run_output_filepath=run.create_run_filepath(
#         interim_common_names_replaced_abstracts_filepath
#     ),
#     entity_type_to_replace="common",
#     seed=SEED,
# )

# interim_pharmaceutical_names_replaced_abstracts_filepath: str = (
#     "data/processed/synthesised_annotated_abstracts/D_pharmaceutical_replaced"
# )
# perform_entity_replacement(
#     run_input_filepath=run.create_run_filepath(
#         interim_common_names_replaced_abstracts_filepath
#     ),
#     run_output_filepath=run.create_run_filepath(
#         interim_pharmaceutical_names_replaced_abstracts_filepath
#     ),
#     entity_type_to_replace="pharmaceutical",
#     seed=SEED,
# )
