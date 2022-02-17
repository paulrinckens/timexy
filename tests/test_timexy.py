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
