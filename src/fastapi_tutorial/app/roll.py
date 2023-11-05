"""Roll dice."""
from random import randint
from typing import Annotated
from annotated_types import Ge, Gt

def roll(d: Annotated[int, Gt(0)], /) -> int:
    return randint(1, d)

def roll_set(set: dict[Annotated[int, Gt(0)], Annotated[int, Ge(0)]], /) -> dict[int, list[int]]:
    return {d: [roll(d) for _ in range(n)] for d, n in set.items()}
