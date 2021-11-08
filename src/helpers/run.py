from datetime import datetime
from pathlib import Path, PosixPath


ARTIFACTS_FILEPATH = "data/run_artifacts/"
LAST_RUN_FILE = "last_run.txt"


class Run:
    def __init__(self):
        self.start_datetime = self.create_run_timestamp()

    def create_run_timestamp(self) -> str:
        return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    def create_run_filepath(self, filepath: str = None) -> PosixPath:
        if not filepath:
            return Path(f"{self.start_datetime}")
        else:
            return Path(f"{filepath}/{self.start_datetime}")
