from pathlib import Path
from glob import glob
import os
import json
import random
from dataclasses import dataclass
from typing import List

from src.helpers.entity_replacement.functions import (
    PhraseLocation,
    replace_phrase_at_location,
)


@dataclass
class SimpleLabel:
    start: int
    end: int
    entity_label: str


@dataclass
class ReplacementEntity:
    text: str
    entity_label: str


@dataclass
class DoccanoAnnotationObject:
    """
    https://spacy.io/api/data-formats
    Option 2: List of "(start, end, label)" tuples defining all entities in the text.
    List[Tuple[int, int, str]]
    """

    id: int
    data: str
    label: List[SimpleLabel]


def perform_entity_replacement(
    run_input_filepath: Path,
    run_output_filepath: Path,
    entity_type_to_replace: str,
    seed: int = 42,
    sample_run: bool = False,
) -> None:

    random.seed(seed)

    # Make sure the output filepath exists
    run_output_filepath.mkdir(parents=True, exist_ok=True)

    if sample_run:
        run_input_filepath = "data/sample_data/sample_mappable_pair3.json"

        with open(run_input_filepath, "r") as f:
            all_mappable_pairs = [json.loads(json_line) for json_line in list(f)]

    else:
        # BUG: I have some issue where I can't get this file location right via glob.
        # As a consequence this stage has to be run in two parts. That's ok for now.
        # TODO: Log this as an issue and move on for now.

        # run_input_filepath_glob = glob(f"{run_input_filepath}/")
        # run_input_filepath_json_glob = glob(f"{run_input_filepath_glob[0]}/*.json")

        # with open(run_input_filepath_json_glob[0], "r") as f:
        #     # for i, line in enumerate(f):
        #     #     try:
        #     #         d = json.loads(line)
        #     #     except json.decoder.JSONDecodeError:
        #     #         print("Error on line", i + 1, ":\n", repr(line))
        #     all_mappable_pairs = [json.loads(json_line) for json_line in list(f)]

        if entity_type_to_replace == "scientific":
            json_file_name: str = (
                "part-00000-e9764264-8bec-44b2-9778-7213d0bc06d8-c000.json"
            )
        else:
            json_file_name: str = "output.json"

        with open(os.path.join(run_input_filepath, json_file_name), "r") as f:
            all_mappable_pairs = [json.loads(json_line) for json_line in list(f)]

    if entity_type_to_replace == "scientific":
        for _mappable_pair in all_mappable_pairs:
            # If mappable entities are empty, e.g. common_names = [],
            # just move on to the next mappable_pair.
            if len(_mappable_pair[entity_type_to_replace + "_entities"]) == 0:
                with open(os.path.join(run_output_filepath, "output.json"), "a+") as f:
                    # Dump updated mappable pair as JSONL
                    f.write(json.dumps(_mappable_pair))
                    f.write("\n")
                continue

            # Hack to fix lists being chewed up by JSON
            fixed_mappable_entities = [
                [
                    int(_.split(",")[0].strip("[")),
                    int(_.split(",")[1].strip()),
                    _.split(",")[2].strip("]").strip(),
                ]
                for _ in _mappable_pair["scientific_entities"]
            ]
            # Transform each mappable item in the mappable pairs JSONL into a DoccanoAnnotationObject.
            original_doccano_annotation = DoccanoAnnotationObject(
                id=_mappable_pair["id"],
                data=_mappable_pair["data"],
                label=fixed_mappable_entities,
            )
            # The following is needed because the labels cannot be
            # relied on to be supplied in order of appearance.
            # Labels here accepts either Lists or Tuples.
            typed_labels = [
                SimpleLabel(*lb) for lb in original_doccano_annotation.label
            ]
            typed_labels.sort(key=lambda x: x.start)

            new_labels = []

            # This is needed to keep a record of all the changes
            # in character positions in the text as entities are replaced.
            corpus_offset = 0
            corpus = original_doccano_annotation.data

            for lb in typed_labels:
                # Get the right replacement entity
                replacement_entity = ReplacementEntity(
                    text=_mappable_pair["scientific_name"],
                    entity_label="scientific",
                )
                # Get location of current label. The corpus_offset is a running count
                # of what it's cost us to move words around so far.
                loc = PhraseLocation(lb.start + corpus_offset, lb.end + corpus_offset)

                (new_phrase, new_loc), new_corpus, _ = (  # noqa: F841
                    *replace_phrase_at_location(loc, corpus, replacement_entity.text),
                    "",
                )

                new_labels.append(
                    [new_loc.start, new_loc.end, replacement_entity.entity_label]
                )
                corpus_offset += new_loc.end - loc.end
                corpus = new_corpus

            # corpus is now final corpus after looping through all the labels

            with open(os.path.join(run_output_filepath, "output.json"), "a+") as f:
                _mappable_pair[
                    "new_" + entity_type_to_replace + "_entities"
                ] = new_labels
                _mappable_pair["data"] = corpus

                # Dump updated mappable pair as JSONL
                f.write(json.dumps(_mappable_pair))
                f.write("\n")

    else:
        for _mappable_pair in all_mappable_pairs:
            # If mappable entities are empty, e.g. common_names = [],
            # just move on to the next mappable_pair.
            if len(_mappable_pair[entity_type_to_replace + "_entities"]) == 0:
                with open(os.path.join(run_output_filepath, "output.json"), "a+") as f:
                    # Dump updated mappable pair as JSONL
                    f.write(json.dumps(_mappable_pair))
                    f.write("\n")
                continue

            # Hack to fix lists being chewed up by JSON
            fixed_mappable_entities = [
                [
                    int(_.split(",")[0].strip("[")),
                    int(_.split(",")[1].strip()),
                    _.split(",")[2].strip("]").strip(),
                ]
                for _ in _mappable_pair[entity_type_to_replace + "_entities"]
            ]
            # Transform each mappable item in the mappable pairs JSONL into a DoccanoAnnotationObject.
            original_doccano_annotation = DoccanoAnnotationObject(
                id=_mappable_pair["id"],
                data=_mappable_pair["data"],
                label=fixed_mappable_entities,
            )
            # The following is needed because the labels cannot be
            # relied on to be supplied in order of appearance.
            # Labels here accepts either Lists or Tuples.
            typed_labels = [
                SimpleLabel(*lb) for lb in original_doccano_annotation.label
            ]
            typed_labels.sort(key=lambda x: x.start)

            new_labels = []

            # This is needed to keep a record of all the changes
            # in character positions in the text as entities are replaced.
            corpus_offset = 0
            corpus = original_doccano_annotation.data

            for lb in typed_labels:
                _selection = random.choice(
                    _mappable_pair[entity_type_to_replace + "_names"]
                )

                # Get the right replacement entity
                replacement_entity = ReplacementEntity(
                    text=_selection["non_scientific_name"],
                    entity_label=entity_type_to_replace,
                )
                # Get location of current label. The corpus_offset is a running count
                # of what it's cost us to move words around so far.
                loc = PhraseLocation(lb.start + corpus_offset, lb.end + corpus_offset)

                (new_phrase, new_loc), new_corpus, _ = (  # noqa: F841
                    *replace_phrase_at_location(loc, corpus, replacement_entity.text),
                    "",
                )

                new_labels.append(
                    [new_loc.start, new_loc.end, replacement_entity.entity_label]
                )
                corpus_offset += new_loc.end - loc.end
                corpus = new_corpus

            # corpus is now final corpus after looping through all the labels

            with open(os.path.join(run_output_filepath, "output.json"), "a+") as f:
                _mappable_pair[
                    "new_" + entity_type_to_replace + "_entities"
                ] = new_labels
                _mappable_pair["data"] = corpus

                # Dump updated mappable pair as JSONL
                f.write(json.dumps(_mappable_pair))
                f.write("\n")
