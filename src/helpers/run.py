from datetime import datetime
from pathlib import Path, PosixPath


ARTIFACTS_FILEPATH = "data/run_artifacts/"
LAST_RUN_FILE = "last_run.txt"


class Run:
    def __init__(self, last_run_timestamp: str = None):
        if last_run_timestamp:
            self.start_datetime: str = last_run_timestamp
        else:
            self.start_datetime: str = self.create_run_timestamp()

    def create_run_timestamp(self) -> str:
        return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    def create_run_filepath(self, filepath: str = None) -> PosixPath:
        if not filepath:
            return Path(f"{self.start_datetime}")
        else:
            return Path(f"{filepath}/{self.start_datetime}")

    def record_last_run_timestamp(self) -> None:
        artifacts_filepath: Path = Path(ARTIFACTS_FILEPATH)
        artifacts_filepath.mkdir(parents=True, exist_ok=True)

        with Path(f"{artifacts_filepath}/{LAST_RUN_FILE}").open("w") as f:
            f.write(self.start_datetime)


def get_last_run_timestamp():
    with Path(f"{ARTIFACTS_FILEPATH}/{LAST_RUN_FILE}").open("r") as f:
        last_run_id: str = f.readline()
    return last_run_id
