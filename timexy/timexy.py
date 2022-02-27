import datetime as dt
import logging
import re
import traceback
from collections import OrderedDict
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Union

import srsly
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from . import util


def _load_cfg(path: Any) -> Dict:
    if path.exists():
        return srsly.read_json(path)
    else:
        return {}


@Language.factory(
    "timexy",
    default_config={"label": "timexy", "kb_id_type": "timex3", "overwrite": False},
)
def make_timexy(
    nlp: Language, name: str, kb_id_type: str, label: str, overwrite: bool
) -> "Timexy":
    return Timexy(
        nlp=nlp, name=name, kb_id_type=kb_id_type, label=label, overwrite=overwrite
    )


class Timexy:

    MAX_LEN_PATTERN = 5

    def __init__(
        self,
        nlp: Language,
        name: str = "timexy",
        kb_id_type: str = "timex3",
        label: str = "time",
        overwrite: bool = False,
    ) -> None:
        self.logger = logging.getLogger(__name__)

        self.lang = nlp.lang
        self.name = name
        self.kb_id_type = kb_id_type
        self.label = label
        self.overwrite = overwrite
        self.cfg = {
            "label": self.label,
            "kb_id_type": self.kb_id_type,
            "overwrite": self.overwrite,
        }

        try:
            self.timexy_lang = getattr(
                import_module(f"timexy.languages.{self.lang}"), self.lang
            )
        except Exception:
            raise NameError(f"Language {self.lang} not supported by timexy")

        self.date_regexes = []
        for date_rule in self.timexy_lang.rules:
            self.date_regexes.append((re.compile(date_rule.regex), date_rule.pattern))

        self.matcher = Matcher(nlp.vocab)
        for key, vals in self.timexy_lang.units.items():
            for val in vals:
                self.matcher.add(
                    key,
                    [[{"IS_DIGIT": True}, {"TEXT": val}]],
                )

                self.matcher.add(
                    key,
                    [
                        [
                            {"LOWER": {"IN": self.timexy_lang.num_words}},
                            {"LOWER": val.lower()},
                        ]
                    ],
                )

    def __call__(self, doc: Doc) -> Doc:
        spans_to_add = self.date_matches(doc) + self.duration_matches(doc)

        # Create entities for all gathered spans
        for span in spans_to_add:

            # ignore match if there is an overlapping entity of another type
            if (
                any(
                    t.ent_type and t.ent_type_ != self.label
                    for t in doc[span.start : span.end]
                )
                and not self.overwrite
            ):
                continue

            # if overlapping entities due to multiple matched date patterns,
            # keep entity with longest span and dump others
            if any(t.ent_type for t in doc[span.start : span.end]):

                # Only look for overlaps +- 5 tokens to left and right as there are no
                # date patterns consisting of more than 5 tokens
                span_ents = doc[
                    max(0, span.start - self.MAX_LEN_PATTERN) : min(
                        span.end + self.MAX_LEN_PATTERN, len(doc)
                    )
                ].ents
                overlap_ents = [
                    e
                    for e in span_ents
                    if span.start_char < e.end_char and span.end_char > e.start_char
                ]
                timexy_overlap_ents = [
                    e for e in overlap_ents if e.label_ == self.label
                ]

                # If overlapping entities of other label, overwrite
                # If overlapping entities with timexy label, only overwrite if span is longer than existing
                if all(len(e) <= len(span) for e in timexy_overlap_ents):
                    doc.ents = [e for e in doc.ents if e not in overlap_ents] + [span]
            else:
                try:
                    doc.ents += (span,)
                except Exception:
                    self.logger.error(
                        f"Unable to set entity {span.text} with offset ({span.start},{span.end}). Skipping this entity."
                    )
                    self.logger.error(traceback.format_exc())

        return doc

    def date_matches(self, doc: Doc) -> List[Span]:
        spans = []
        for regex in self.date_regexes:
            for m in regex[0].finditer(doc.text):
                end_offset = m.span()[1]
                # if next character is a digit this is likely not a date, skip match
                if len(doc.text) > end_offset and doc.text[end_offset].isdigit():
                    continue
                try:
                    # convert written months (%b and %B) back to numbers based on
                    # language class to allow parsing without need to install any locale
                    datestring, date_format = self._replace_month_str(
                        m.group(0), regex[1]
                    )
                    d = dt.datetime.strptime(datestring, date_format)
                except Exception:
                    self.logger.info(
                        f"Error during parsing of date for match {str(m.group(0))} with character offset {str(m.span())}. Skipping the match."
                    )
                    continue

                span = doc.char_span(
                    *m.span(),
                    label=self.label,
                    kb_id=self._get_date_kb_id(d, self.kb_id_type),
                )

                if span:
                    spans.append(span)
                else:
                    self.logger.error(
                        f"Span could not be retrieved for annotation of type {self.label} for datestring {datestring} with character offsets {m.span()}. Skipping the match."
                    )
        return spans

    def duration_matches(self, doc: Doc) -> List[Span]:
        spans = []
        matches = self.matcher(doc)
        for match_id, start, end in matches:

            if any(t.ent_type for t in doc[start:end]) and not self.overwrite:
                continue

            dur_unit = doc.vocab.strings[match_id]
            cnt_token = Span(doc, start, end)[0]
            if cnt_token.is_digit:
                cnt = cnt_token.text
            else:
                cnt = self.timexy_lang.num_words.index(cnt_token.text.lower())
            if cnt:
                kb_id = self._get_duration_kb_id(cnt, dur_unit)
                ent = Span(doc, start, end, label=self.label, kb_id=kb_id)
                spans.append(ent)
        return spans

    def _replace_month_str(self, datestring: str, date_format: str) -> Tuple[str, str]:
        """
        Replace all months strings in the specified datestring with their index
        (e.g. February --> 2) and return the updated datesting and date_format.
        The replacement is case-insensitive.
        """
        if "%b" in date_format or "%B" in date_format:
            sorted_month_str_pairs = sorted(
                self.timexy_lang.get_month_str_pairs(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
            for month_str_pair in sorted_month_str_pairs:
                if month_str_pair[1].lower() in datestring.lower():
                    datestring = datestring.lower().replace(
                        month_str_pair[1].lower(), str(month_str_pair[0])
                    )
                    date_format = date_format.replace("%b", "%m").replace("%B", "%m")
                    return datestring, date_format
        return datestring, date_format

    def _get_date_kb_id(self, d: dt.datetime, kb_id_type: str) -> str:
        if kb_id_type == "timex3":
            return f'TIMEX3 type="DATE" value="{d.isoformat()}"'
        elif kb_id_type == "timestamp":
            return str(d.timestamp())
        else:
            raise ValueError(f"Illegal argument for kb_id_type: {kb_id_type}")

    def _get_duration_kb_id(self, cnt: str, unit: str) -> str:
        return f'TIMEX3 type="DURATION" value="P{cnt}{unit}"'

    def to_disk(self, path: Union[str, Path], *, exclude: Iterable[str] = []) -> None:
        serialize = OrderedDict()
        serialize["cfg"] = lambda p: srsly.write_json(p, self.cfg)

        util.to_disk(path, serialize, exclude)

    def from_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = []
    ) -> "Timexy":
        deserialize = {}
        deserialize["cfg"] = lambda p: self.cfg.update(_load_cfg(p))

        util.from_disk(path, deserialize, exclude)

        return self
