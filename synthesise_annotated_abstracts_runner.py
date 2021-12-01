from pathlib import Path
from pyspark.sql import SparkSession

from src.helpers.run import Run, get_last_run_timestamp
from src.F_synthesise_annotated_abstracts.synthesise_annotated_abstracts import (
    synthesise_annotated_abstracts,
)
from src.helpers.train_test_split import TrainTestSplit


TRAIN_TEST_SPLIT = TrainTestSplit(0.5, 0.5)

spark = SparkSession.builder.appName("run_ner_pipeline").getOrCreate()
run = Run(last_run_timestamp=get_last_run_timestamp())

split_annotated_abstracts_filepath: str = "data/processed/split_annotated_abstracts"
name_mappings_filepath: str = "data/reference/mpns_v8/mpns_name_mappings/v3"
synthesised_annotated_abstracts_filepath: str = (
    "data/processed/synthesised_annotated_abstracts"
)
synthesise_annotated_abstracts(
    spark=spark,
    run_input_filepath=run.create_run_filepath(split_annotated_abstracts_filepath),
    name_mappings_filepath=Path(name_mappings_filepath),
    run_output_filepath=run.create_run_filepath(
        synthesised_annotated_abstracts_filepath
    ),
    train_test_split=TRAIN_TEST_SPLIT,
    split_subset_type="train",
    seed=1,
)

# synthesise_annotated_abstracts(
#     spark=spark,
#     run_input_filepath=run.create_run_filepath(split_annotated_abstracts_filepath),
#     name_mappings_filepath=Path(name_mappings_filepath),
#     run_output_filepath=run.create_run_filepath(
#         synthesised_annotated_abstracts_filepath
#     ),
#     train_val_test_split=TRAIN_VAL_TEST_SPLIT,
#     split_subset_type="validation",
#     seed=2,
# )
