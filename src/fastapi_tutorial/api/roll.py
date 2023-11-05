"""API for app/roll.py"""
from functools import reduce
from operator import mul as _mul
from typing import Annotated, Callable, Iterable, Literal
from annotated_types import Ge, Gt
from fastapi import APIRouter

from .utils.result import result
from .utils.errors import handle, validate_call
from ..app import roll as core

def mul[N: float](it: Iterable[N]) -> N:
    return reduce(_mul, it, 1)


router = APIRouter(prefix="/roll")

@router.get("/d{die}")
@validate_call()
@result
def roll(die: Annotated[int, Gt(0)]) -> int:
    return core.roll(die)


_OP: dict[str, Callable[[Iterable[int]], int]] = {
    "sum": sum,
    "mul": mul,
}

@router.get("/{n}d{die}")
@validate_call()
@result
def roll_multi(n: Annotated[int, Ge(0)], die: Annotated[int, Gt(0)], op: Literal["sum", "mul"] = "sum") -> int:
    return _OP[op](core.roll(die) for _ in range(n))


def _parse_die(s: str) -> tuple[int, int]:
    n, d = s.strip().split("d")
    return int(n or "1"), int(d)


_core_roll_set = validate_call(handle=False)(core.roll_set)

@router.get("/set/{set}")
@validate_call()
@handle(ValueError)
@result
def roll_diceset(set: str) -> dict[int, list[int]]:
    dice: dict[int, int] = {}
    for n, d in map(_parse_die, set.split(",")):
        if d not in dice:
            dice[d] = 0
        dice[d] += n
    return _core_roll_set(dice)


__all__ = [
    "router", "roll", "roll_multi", "roll_diceset",
]
