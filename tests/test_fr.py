import pytest
import spacy
from spacy.language import Language

from timexy.languages.fr import fr

label = "timexy_label"
lang = "fr"


@pytest.fixture()
def nlp() -> Language:
    nlp = spacy.blank(lang)
    nlp.add_pipe("timexy", config={"label": label})
    return nlp


test_data = [t for rule in fr.rules for t in rule.tests]


@pytest.mark.parametrize("text,date_start,date_end", test_data)
def test_rule(nlp: Language, text: str, date_start: int, date_end: int) -> None:
    doc = nlp(text)
    assert [
        e
        for e in doc.ents
        if e.start_char == date_start and e.end_char == date_end and e.label_ == label
    ]
