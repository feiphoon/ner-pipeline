import random
import json
import math
from pathlib import Path

from src.helpers.train_test_split import TrainTestSplit, check_valid_split


def split_for_train_and_val(
    run_input_filepath: Path,
    run_output_filepath: Path,
    train_val_split: TrainTestSplit,
    seed: int = 42,
) -> None:
    check_valid_split(train_val_split)
    random.seed(seed)

    # TODO: Included the filename here as a hack, glob not working
    with open(
        Path(
            f"{run_input_filepath}/part-00000-88912f79-07bd-4a96-89d6-013fe0fe394c-c000.json"
        ),
        "rb",
    ) as f:
        data: list = [json.loads(json_line) for json_line in list(f)]

    _num_rows: int = len(data)

    random.shuffle(data)

    _train_num_rows: int = math.ceil(_num_rows * train_val_split.train)
    train_data: list = data[:_train_num_rows]
    val_data: list = data[_train_num_rows:]

    # Make sure the output filepaths exist
    run_output_filepath_train: Path = Path(f"{run_output_filepath}/train")
    run_output_filepath_val: Path = Path(f"{run_output_filepath}/dev")

    run_output_filepath.mkdir(parents=True, exist_ok=True)
    run_output_filepath_train.mkdir(parents=True, exist_ok=True)
    run_output_filepath_val.mkdir(parents=True, exist_ok=True)

    # Then write split data
    with open(Path(f"{run_output_filepath_train}/train.json"), "w+") as f:
        f.write(json.dumps(train_data))
        f.write("\n")

    with open(Path(f"{run_output_filepath_val}/dev.json"), "w+") as f:
        f.write(json.dumps(val_data))
        f.write("\n")

    _metadata: dict = {
        "source_line_count": _num_rows,
        "train_line_count": _train_num_rows,
        "val_line_count": (_num_rows - _train_num_rows),
    }

    with Path(f"{run_output_filepath}/process_metadata.json").open(
        "w+", encoding="utf-8"
    ) as file:
        json.dump(_metadata, file)
