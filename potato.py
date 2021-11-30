from pathlib import Path
from glob import glob
from zipfile import ZipFile


run_input_filepath = Path("data/processed/annotated_abstracts/2021-11-30-12-09-58")

run_input_filepath_glob = glob(f"{run_input_filepath}/")
print(run_input_filepath_glob)
run_input_filepath_zip_glob = glob(f"{run_input_filepath_glob[0]}/*.zip")

with ZipFile(run_input_filepath_zip_glob[0], "r") as zip_f:
    zip_f.extractall(run_input_filepath_glob[0])
