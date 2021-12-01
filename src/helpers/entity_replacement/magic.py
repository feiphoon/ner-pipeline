import json
import random
from dataclasses import dataclass
from typing import List

from src.helpers.entity_replacement.functions import PhraseLocation, replace_phrase_at_location


@dataclass
class SimpleLabel:
    start: int
    end: int
    entity_label: str


@dataclass
class ReplacementEntity:
    text: str
    text_length: int
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


random.seed(42)

INPUTFILEPATH = "../../../data/sample_data/sample_mappable_pair2.json"
ENTITY_TYPE_TO_REPLACE = "scientific"

with open(INPUTFILEPATH, "r") as f:
    all_mappable_pairs = [json.loads(json_line) for json_line in list(f)]


# Get the right replacement entity
# if ENTITY_TYPE_TO_REPLACE == "scientific":
#     replacement_entity = ReplacementEntity(
#         text=_mappable_pair["scientific_name"],
#         text_length=_mappable_pair["scientific_name_length"],
#         entity_label="scientific",
#     )
# elif ENTITY_TYPE_TO_REPLACE == "common":
#     _selection = random.choice(_mappable_pair["common_names"])

#     replacement_entity = ReplacementEntity(
#         text=_selection["non_scientific_name"],
#         text_length=_selection["non_scientific_name_length"],
#         entity_label="common",
#     )
# elif ENTITY_TYPE_TO_REPLACE == "pharmaceutical":
#     _selection = random.choice(_mappable_pair["pharmaceutical_names"])

#     replacement_entity = ReplacementEntity(
#         text=_selection["non_scientific_name"],
#         text_length=_selection["non_scientific_name_length"],
#         entity_label="pharmaceutical",
#     )

if ENTITY_TYPE_TO_REPLACE == "scientific":
    for _mappable_pair in all_mappable_pairs:
        # Get the right replacement entity
        replacement_entity = ReplacementEntity(
            text=_mappable_pair["scientific_name"],
            text_length=_mappable_pair["scientific_name_length"],
        )

        # Transform each mappable item in the mappable pairs JSONL into a DoccanoAnnotationObject.
        original_doccano_annotation = DoccanoAnnotationObject(
            id=_mappable_pair["id"],
            data=_mappable_pair["data"],
            label=_mappable_pair["scientific_labels"],
        )

        # The following is needed because the labels cannot be
        # relied on to be supplied in order of appearance.
        # Labels here accepts either Lists or Tuples.
        typed_labels = [SimpleLabel(*lb) for lb in original_doccano_annotation.label]
        typed_labels.sort(key=lambda x: x.start)

        new_labels = []

        # This is needed to keep a record of all the changes
        # in character positions in the text as entities are replaced.
        corpus_offset = 0
        corpus = original_doccano_annotation.data

        for lb in typed_labels:
            # We always want to know the location of EVERY label item, regardless of if we will shift it.
            loc = PhraseLocation(lb.start + corpus_offset, lb.end + corpus_offset)
            # Check the entity_label attribute of the label item
            if lb.entity_label == ENTITY_TYPE_TO_REPLACE:

            original_phrase = return_phrase_at_location(loc, corpus)
            annotation = lb.entity_label
            # TODO: Replace this with the label of the replacement entity.

            (new_phrase, new_loc), new_corpus, _ = (
                *replace_phrase_at_location(loc, corpus, "banana"),
                "",
            )  # TODO: Replace "banana" string later with the new entity string.

            # TODO: Replace the annotation with the label of the replacement entity.
            new_labels.append([new_loc.start, new_loc.end, annotation])
            corpus_offset += new_loc.end - loc.end
            corpus = new_corpus
