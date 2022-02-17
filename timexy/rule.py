from typing import List, Tuple

from pydantic import BaseModel


class Rule(BaseModel):
    regex: str
    pattern: str
    tests: List[Tuple[str, int, int]]
