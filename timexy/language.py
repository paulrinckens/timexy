import itertools
from typing import Dict, List, Tuple

from pydantic import BaseModel

from .rule import Rule


class Language(BaseModel):
    lang: str
    months: List[List[str]]
    units: Dict["str", List[str]]
    num_words: List[str]
    rules: List[Rule] = []

    def get_month_re(self) -> str:
        return "|".join(
            itertools.chain(
                *self.months,
                [s.upper() for s in itertools.chain.from_iterable(self.months)],
            )
        )

    def get_month_str_pairs(self) -> List[Tuple[int, str]]:
        month_str_pairs = []
        for month_idx, month_strs in enumerate(self.months):
            month_str_pairs.extend([(month_idx + 1, m) for m in month_strs])
        return month_str_pairs
