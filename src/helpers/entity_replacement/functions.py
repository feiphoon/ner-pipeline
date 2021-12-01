import re
from dataclasses import dataclass
from typing import List, Union, Tuple

# annotation_dict1 = {
#     "id": 1,
#     "data": "Hey I like this Aerva sanguinolenta (L.) Blume as it's super cute. I think we have potatoes in England.\n", # noqa: E501
#     "label": [
#         [16, 46, "scientific name"],
#         [85, 94, "common name"],
#         [85, 92, "location"],
#     ],
# }

# test_text = "I love bananas, but I hate pineapple."


@dataclass
class PhraseLocation:
    start: int = None
    end: int = None


def check_corpus_provided(corpus: str):
    assert corpus, "No corpus provided."


def check_target_provided(target: str):
    assert target, "No target provided."


class PhraseLocationOutOfBoundsError(Exception):
    pass


def check_phrase_is_within_bounds(loc: PhraseLocation, corpus: str):
    if not (corpus_len := len(corpus) >= loc.end):
        raise PhraseLocationOutOfBoundsError(
            f"PhraseLocation out of bounds of corpus length. "
            f"Corpus length: {corpus_len},"
            f"requested PhraseLocation at [{loc.start}, {loc.end}]."
        )


def check_phraselocation_valid(loc: PhraseLocation, corpus: str):
    assert loc, "No PhraseLocation provided."
    assert loc.start is not None, "No PhraseLocation start value provided."
    assert loc.end is not None, "No PhraseLocation end value provided."
    check_phrase_is_within_bounds(loc, corpus)
    assert loc.start >= 0, f"PhraseLocation less than 0 - {loc.start}."


def return_location_of_phrase(
    target: str = "", corpus: str = ""
) -> List[PhraseLocation]:
    check_target_provided(target)
    check_corpus_provided(corpus)
    loc_list = []
    for match in re.finditer(re.escape(target) + "s?", corpus):
        loc_list.append(PhraseLocation(match.start(), match.end()))
    return loc_list


def return_phrase_at_location(loc: PhraseLocation, corpus: str) -> str:
    check_corpus_provided(corpus)
    check_phraselocation_valid(loc, corpus)
    return corpus[loc.start : loc.end]


def replace_phrase_at_location(
    loc: PhraseLocation, corpus: str, replace_with: str
) -> Union[Tuple[str, PhraseLocation], str]:
    """
    https://stackoverflow.com/questions/14895599/insert-an-element-at-a-specific-index-in-a-list-and-return-the-updated-list
    """
    # TODO: Move these checks out of these methods
    # - do them once in whatever parent process.
    check_corpus_provided(corpus)
    check_phraselocation_valid(loc, corpus)
    check_target_provided(replace_with)

    phrase_to_replace = return_phrase_at_location(loc, corpus)

    phrase_to_replace_start_idx = loc.start
    phrase_to_replace_end_idx = len(phrase_to_replace) + loc.start

    # We can't use replace() because the phrase is down to a
    # phrase at a specific location
    corpus = list(corpus)

    del corpus[phrase_to_replace_start_idx:phrase_to_replace_end_idx]
    corpus[phrase_to_replace_start_idx:phrase_to_replace_start_idx] = replace_with

    replacement_phrase_idx = phrase_to_replace_start_idx + len(replace_with)

    # TODO: This will probably be structured better later
    # TODO: Take out the conversion to list and back for faster processing.
    return (
        (
            replace_with,
            PhraseLocation(phrase_to_replace_start_idx, replacement_phrase_idx),
        ),
        "".join(corpus),
    )
