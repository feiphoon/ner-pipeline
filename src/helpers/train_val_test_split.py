from dataclasses import dataclass


@dataclass
class TrainValTestSplit:
    train: float
    val: float
    test: float


class InvalidSplitError(Exception):
    pass


def check_valid_split(split_config: TrainValTestSplit) -> bool:
    if (split_config.train + split_config.val + split_config.test) != 1:
        raise InvalidSplitError("Split config must add up to 1.")
