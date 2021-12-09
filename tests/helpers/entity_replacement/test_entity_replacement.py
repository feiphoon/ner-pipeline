from pathlib import Path
from src.F_synthesise_annotated_abstracts.entity_replacement import (
    perform_entity_replacement,
)

import os


def test_entity_replacement():
    print(os.listdir())
    SEED = 42
    perform_entity_replacement(
        run_input_filepath=Path("tests/helpers/entity_replacement/fixtures/"),
        run_output_filepath=Path("tests/helpers/entity_replacement/fixtures/out/"),
        entity_type_to_replace="common",
        seed=SEED,
    )


import re
