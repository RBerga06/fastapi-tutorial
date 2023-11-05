from functools import wraps
from inspect import signature
from typing import Callable, TypedDict, final

@final
class Result[T](TypedDict):
    result: T


def result[**P, R](f: Callable[P, R]) -> Callable[P, Result[R]]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R]:
        return Result(result=f(*args, **kwargs))
    # Fix signature
    sig = signature(wrapper)
    wrapper.__signature__ = sig.replace(return_annotation=Result[sig.return_annotation])  # type: ignore
    return wrapper