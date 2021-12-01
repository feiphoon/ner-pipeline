import json
from dataclasses import dataclass
from typing import List

from src.helpers.entity_replacement.functions import (
    PhraseLocation,
    replace_phrase_at_location,
    return_phrase_at_location,
)


@dataclass
class SimpleLabel:
    start: int
    end: int
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


with open("all.jsonl", "r") as f:
    all_annotations = [json.loads(json_line) for json_line in list(f)]

for _ in all_annotations:
    # Transform each item in the annotations JSONL into a DoccanoAnnotationObject.
    original_doccano_annotation = DoccanoAnnotationObject(**_)
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
        loc = PhraseLocation(lb.start + corpus_offset, lb.end + corpus_offset)
        phrase = return_phrase_at_location(loc, corpus)
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

    # corpus is now final corpus after looping through all the labels
    new_doccano_annotation = DoccanoAnnotationObject(
        id=original_doccano_annotation.id,
        data=corpus,
        label=new_labels,
    )

    with open("new.jsonl", "a+") as f:
        # Convert Doccano Annotation to dict
        new_annotation_dict = {
            "id": new_doccano_annotation.id,
            "data": new_doccano_annotation.data,
            "label": new_doccano_annotation.label,
        }
        # Dump annotation as JSONL
        f.write(json.dumps(new_annotation_dict))
        f.write("\n")

