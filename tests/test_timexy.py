import datetime as dt

import pytest
import spacy

from timexy.timexy import Timexy


def test_supported_lang() -> None:
    nlp = spacy.blank("en")
    t = Timexy(nlp, "timexy", "timex3", "label")
    assert t


def test_unsupported_lang() -> None:
    nlp = spacy.blank("xx")
    with pytest.raises(NameError):
        Timexy(nlp, "timexy", "timex3", "label")


@pytest.mark.parametrize(
    "datestring, date_format, datestring_expected, date_format_expected",
    [
        ("3 February 2010", "%d %B %Y", "3 2 2010", "%d %m %Y"),
        ("3. Mar 2020", "%d. %b %Y", "3. 3 2020", "%d. %m %Y"),
    ],
)
def test_replace_month_str(
    datestring: str,
    date_format: str,
    datestring_expected: str,
    date_format_expected: str,
) -> None:
    timexy = Timexy(spacy.blank("en"))
    datestring_new, date_format_new = timexy._replace_month_str(datestring, date_format)
    assert datestring_expected == datestring_new
    assert date_format_expected == date_format_new


def test_kb_id_timestamp() -> None:
    nlp = spacy.blank("en")
    config = {"kb_id_type": "timestamp", "label": "timexy", "overwrite": False}
    nlp.add_pipe("timexy", config=config)
    text = "Today is the 01.01.1990, the first day of the year 1990."
    doc = nlp(text)
    assert doc.ents
    assert doc.ents[0].kb_id_ == str(
        dt.datetime.strptime("01.01.1990", "%d.%m.%Y").timestamp()
    )


def test_kb_id_timex3() -> None:
    nlp = spacy.blank("en")
    config = {"kb_id_type": "timex3", "label": "timexy", "overwrite": False}
    nlp.add_pipe("timexy", config=config)
    text = "Today is the 01.01.1990, six years after 01.01.1984."
    doc = nlp(text)
    assert doc.ents
    assert doc.ents[1].kb_id_ == 'TIMEX3 type="DURATION" value="P6Y"'


def test_overwrite_date_true() -> None:
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {
            "label": "EXISTING_ENT",
            "pattern": [{"LOWER": "is"}, {"LOWER": "feb"}],
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe("timexy", config={"overwrite": True})
    text = "Today is Feb 1990, six years after Feb 1984."
    doc = nlp(text)
    assert len(doc.ents) == 3
    assert doc[1].ent_type == 0
    assert doc[2].ent_type_ == "timexy"
    assert doc.ents[0].text == "Feb 1990"
    assert doc.ents[1].text == "six years"
    assert doc.ents[2].text == "Feb 1984"


def test_overwrite_date_false() -> None:
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {
            "label": "EXISTING_ENT",
            "pattern": [{"LOWER": "is"}, {"LOWER": "feb"}],
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe("timexy", config={"overwrite": False})
    text = "Today is Feb 1990, six years after Feb 1984."
    doc = nlp(text)
    assert len(doc.ents) == 3
    assert doc[1].ent_type_ == "EXISTING_ENT"
    assert doc[2].ent_type_ == "EXISTING_ENT"
    assert doc.ents[0].text == "is Feb"
    assert doc.ents[1].text == "six years"
    assert doc.ents[2].text == "Feb 1984"


def test_overwrite_duration_true() -> None:
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {
            "label": "EXISTING_ENT",
            "pattern": [{"LOWER": "took"}, {"LOWER": "six"}, {"LOWER": "years"}],
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe("timexy", config={"overwrite": True})
    text = "It took six years."
    doc = nlp(text)
    assert len(doc.ents) == 1
    assert doc[1].ent_type == 0
    assert doc[2].ent_type_ == "timexy"
    assert doc[3].ent_type_ == "timexy"
    assert doc.ents[0].text == "six years"


def test_overwrite_duration_false() -> None:
    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [
        {
            "label": "EXISTING_ENT",
            "pattern": [{"LOWER": "took"}, {"LOWER": "six"}, {"LOWER": "years"}],
        }
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe("timexy", config={"overwrite": False})
    text = "It took six years."
    doc = nlp(text)
    assert len(doc.ents) == 1
    assert doc[1].ent_type_ == "EXISTING_ENT"
    assert doc[2].ent_type_ == "EXISTING_ENT"
    assert doc[3].ent_type_ == "EXISTING_ENT"
    assert doc.ents[0].text == "took six years"
