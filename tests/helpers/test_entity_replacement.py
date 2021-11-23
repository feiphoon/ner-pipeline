import pytest
from src.helpers.entity_replacement import (
    PhraseLocation,
    check_corpus_provided,
    check_phraselocation_valid,
    check_target_provided,
    return_location_of_phrase,
    return_phrase_at_location,
    replace_phrase_at_location,
    PhraseLocationOutOfBoundsError,
)


class TestReturnLocationOfPhrase:
    def test_return_location_of_phrase__single_result(self):
        corpus = "Potatoes."
        result = return_location_of_phrase("Potatoes", corpus)
        expected = [PhraseLocation(0, 8)]
        assert result == expected

    def test_return_location_of_phrase__multi_result(self):
        corpus = "Potatoes. I love Potatoes."
        result = return_location_of_phrase("Potatoes", corpus)
        expected = [PhraseLocation(0, 8), PhraseLocation(17, 25)]
        assert result == expected

    def test_return_location_of_phrase__no_result(self):
        corpus = "Potatoes."
        result = return_location_of_phrase("Bananas", corpus)
        expected = []
        assert result == expected

    def test_return_location_of_phrase__no_result_case_sensitive(self):
        corpus = "Potatoes."
        result = return_location_of_phrase("potatoes", corpus)
        expected = []
        assert result == expected

    def test_return_location_of_phrase__single_result_regex_unfriendly(self):
        corpus = "Potatoes (A.B. Jacks. & Dallim.) Dallim."
        result = return_location_of_phrase(
            "Potatoes (A.B. Jacks. & Dallim.) Dallim.", corpus
        )
        expected = [PhraseLocation(0, 40)]
        assert result == expected

    def test_return_location_of_phrase__no_target_error(self):
        corpus = "Corpus"
        with pytest.raises(AssertionError, match="No target provided."):
            return_location_of_phrase(None, corpus)

    def test_return_location_of_phrase__no_corpus_error(self):
        with pytest.raises(AssertionError, match="No corpus provided."):
            return_location_of_phrase("C", None)

    def test_return_location_of_phrase__empty_corpus_error(self):
        with pytest.raises(AssertionError, match="No corpus provided."):
            return_location_of_phrase("C")


class TestReturnPhraseAtLocation:
    def test_return_phrase_at_location__success(self):
        corpus = "Potatoes."
        result = return_phrase_at_location(PhraseLocation(0, 8), corpus)
        expected = "Potatoes"
        assert result == expected

    def test_return_phrase_at_location__corpus_same_length_as_location(self):
        corpus = "Potatoes."
        result = return_phrase_at_location(PhraseLocation(0, len(corpus)), corpus)
        expected = corpus
        assert result == expected

    def test_return_phrase_at_location__phraselocation_end_OOB(self):
        corpus = "Potatoes."
        with pytest.raises(
            PhraseLocationOutOfBoundsError,
            match="PhraseLocation out of bounds of corpus length.",
        ):
            return_phrase_at_location(PhraseLocation(8, 100), corpus)

    def test_return_phrase_at_location__phraselocation_start_OOB(self):
        corpus = "Potatoes."
        with pytest.raises(
            AssertionError,
            match="PhraseLocation less than 0",
        ):
            return_phrase_at_location(PhraseLocation(-3, 8), corpus)

    def test_return_phrase_at_location__phraselocation_start_not_provided(self):
        corpus = "Potatoes."
        with pytest.raises(
            AssertionError,
            match="No PhraseLocation start value provided.",
        ):
            return_phrase_at_location(PhraseLocation(None, 8), corpus)

    def test_return_phrase_at_location__phraselocation_end_not_provided(self):
        corpus = "Potatoes."
        with pytest.raises(
            AssertionError,
            match="No PhraseLocation end value provided.",
        ):
            return_phrase_at_location(PhraseLocation(0, None), corpus)


class TestReplacePhraseAtLocation:
    def test_replace_phrase_at_location(self):
        corpus = "Hello my name is Slim Shady."

        # Target phrase is "Slim"
        loc = PhraseLocation(17, 21)

        replace_with = "Skinny"
        expected = (
            ("Skinny", PhraseLocation(17, 23)),
            "Hello my name is Skinny Shady.",
        )

        result = replace_phrase_at_location(loc, corpus, replace_with)
        assert result == expected


class TestAssertionErrors:
    @pytest.mark.parametrize("corpus, expected", [("text", None)])
    def test_check_corpus_provided__pass(self, corpus, expected):
        assert check_corpus_provided(corpus) == expected

    @pytest.mark.parametrize(
        "corpus, expected_error", [(None, AssertionError), ("", AssertionError)]
    )
    def test_check_corpus_provided__fail(self, corpus, expected_error):
        with pytest.raises(expected_error, match="No corpus provided."):
            check_corpus_provided(corpus)

    @pytest.mark.parametrize("target, expected", [("text", None)])
    def test_check_target_provided__pass(self, target, expected):
        assert check_target_provided(target) == expected

    @pytest.mark.parametrize(
        "target, expected_error", [(None, AssertionError), ("", AssertionError)]
    )
    def test_check_target_provided__fail(self, target, expected_error):
        with pytest.raises(expected_error, match="No target provided."):
            check_target_provided(target)

    @pytest.mark.parametrize(
        "loc, corpus, expected", [(PhraseLocation(0, 2), "Banana", None)]
    )
    def test_check_phraselocation_valid__success(self, loc, corpus, expected):
        assert check_phraselocation_valid(loc, corpus) == expected

    @pytest.mark.parametrize(
        "loc, corpus, expected_error, expected_message",
        [
            (None, "", AssertionError, "No PhraseLocation provided."),
            (
                PhraseLocation(None, 1),
                "",
                AssertionError,
                "No PhraseLocation start value provided.",
            ),
            (
                PhraseLocation(0, None),
                "",
                AssertionError,
                "No PhraseLocation end value provided.",
            ),
            (
                PhraseLocation(0, 100),
                "B",
                PhraseLocationOutOfBoundsError,
                "PhraseLocation out of bounds of corpus length.",
            ),
            (
                PhraseLocation(-1, 1),
                "Corpus",
                AssertionError,
                "PhraseLocation less than 0",
            ),
        ],
    )
    def test_check_phraselocation_valid__fail(
        self, loc, corpus, expected_error, expected_message
    ):
        with pytest.raises(expected_error, match=expected_message):
            check_phraselocation_valid(loc, corpus)
