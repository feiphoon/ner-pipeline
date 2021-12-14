from pathlib import Path

from src.helpers.run import Run, get_last_run_timestamp
from src.helpers.train_test_split import TrainTestSplit
from src.helpers.run import Run, get_last_run_timestamp

from src.G_prepare_synthetic_annotations_for_ner.split_synthesised_data_for_train_and_val import (
    split_for_train_and_val,
)

TRAIN_VAL_SPLIT = TrainTestSplit(
    0.83, 0.17
)  # works out at a 50%:10%:40% split of abstracts
SEED = 1

run = Run(last_run_timestamp=get_last_run_timestamp())

run_input_filepath: str = "data/processed/synthesised_annotated_abstracts/C_final"
run_output_filepath: str = "data/processed/synthesised_abstracts_for_ner"

split_for_train_and_val(
    run_input_filepath=run.create_run_filepath(run_input_filepath),
    run_output_filepath=run.create_run_filepath(run_output_filepath),
    train_val_split=TRAIN_VAL_SPLIT,
    seed=SEED,
)
