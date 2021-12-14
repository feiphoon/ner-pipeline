"""
This code is to convert JSON data to binary format for spaCy model training.
Was not able to use the spaCy CLI conversion tool - this did not work.
Tried so hard to find something compatible - the following worked correctly and
was a base for this code. Modifications were made so I could debug some issues from upstream.

https://zachlim98.github.io/me/2021-03/spacy3-ner-tutorial
https://spacy.io/usage/training#config
"""
import json
import jsonlines
import os
import random
import spacy
from spacy.tokens import DocBin


def convert_json_to_spacy_format(file_type: str) -> None:

    nlp = spacy.load("en_core_web_trf")

    db = DocBin()

    with open(f"data/{file_type}/{file_type}.json", "r") as f:
        data = json.load(f)

    DATA = []

    for d in data:
        new_anno = []

        if file_type == "test":
            _entities = d["label"]
        else:
            _entities = d["entities"]

        for anno in _entities:
            st, end, label = anno
            new_anno.append((int(st), int(end), label))

        # new_anno.sort(key=lambda x: x[0])  # Sort by start location
        DATA.append((d["data"], {"entities": new_anno}))

    # Disable the pipeline components we don't need
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    ner = nlp.get_pipe("ner")

    # Add custom labels
    labels = ["common", "scientific", "pharmaceutical"]

    for lb in labels:
        ner.add_label(lb)

    # Check that these labels were added
    # print(ner.move_names)

    with nlp.disable_pipes(*other_pipes):
        random.shuffle(DATA)

        for text, annotation in DATA:
            doc = nlp.make_doc(text)

            ents = []

            with open(f"data/{file_type}/{file_type}_conversion_issues.log", "w+") as f:
                for start, end, label in annotation["entities"]:
                    span = doc.char_span(
                        start, end, label=label, alignment_mode="expand"
                    )
                    if span is None:
                        # Log skipped entities
                        f.write(
                            f"Skipping entity. start: {start}, end: {end}, label: {label}, text: {text}\n"
                        )
                        pass
                    else:
                        ents.append(span)
                try:
                    doc.ents = ents  # label the text with the ents
                except ValueError as e:
                    # Log errors
                    f.write(f"{e}. Skipping labelling text. ents: {ents}\n")
                    pass
                else:
                    # Log other exceptions
                    f.write(
                        f"An unknown problem occurred, and the entity was not added. ents: {ents}\n"  # noqa: E501
                    )
                    pass
                db.add(doc)

        db.to_disk(f"data/{file_type}/{file_type}.spacy")  # save the docbin object


def convert_jsonl_to_json(filepath: str, filename: str, data_type: str) -> None:
    with jsonlines.open(os.path.join(filepath, filename), "r") as f:
        json_list: list = []
        for _ in f:
            json_list.append(_)

    with open(os.path.join(filepath, f"{data_type}.json"), "w") as f:
        json.dump(json_list, f)


convert_json_to_spacy_format("train")
convert_json_to_spacy_format("dev")
convert_jsonl_to_json(
    filepath="data/test",
    filename="part-00000-c89cb926-5be3-4c52-a27a-cf9d031475b9-c000.json",
    data_type="test",
)
convert_json_to_spacy_format("test")
