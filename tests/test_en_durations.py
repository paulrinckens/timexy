import pytest
import spacy
from spacy.language import Language

label = "timexy_label"
lang = "en"


@pytest.fixture()
def nlp() -> Language:
    nlp = spacy.blank(lang)
    nlp.add_pipe("timexy", config={"label": label})
    return nlp


def test_digit_years(nlp: Language) -> None:
    doc = nlp("I will try that in 1 year and 2 years")

    for e in doc.ents:
        assert e.label_ == label


def test_word_years(nlp: Language) -> None:
    doc = nlp("I will try that in one year and two years")

    for e in doc.ents:
        assert e.label_ == label


def test_digit_hyphen_years(nlp: Language) -> None:
    doc = nlp("1-year repeat is ideal.")

    assert len(doc.ents) == 1
    assert doc.ents[0].label_ == label


def test_word_hyphen_years(nlp: Language) -> None:
    doc = nlp("one-year repeat is ideal.")

    assert len(doc.ents) == 1
    assert doc.ents[0].label_ == label


def test_digit_hours(nlp: Language) -> None:
    doc = nlp("repeat in 48-72 hours")

    assert len(doc.ents) == 1
    assert doc.ents[0].label_ == label


def test_word_hours(nlp: Language) -> None:
    doc = nlp("I will try that in one hour and two hours")
    print(doc.ents)

    assert len(doc.ents) == 2
    for e in doc.ents:
        assert e.label_ == label
