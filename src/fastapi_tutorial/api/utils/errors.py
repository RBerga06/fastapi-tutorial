from contextlib import contextmanager
import json
from traceback import format_exc
from typing import Any, Callable, Iterator
from fastapi import HTTPException, status
from pydantic import ValidationError, validate_call as _validate_call


@contextmanager
def handle(Exc: type[BaseException], status: int = status.HTTP_404_NOT_FOUND, /) -> Iterator[None]:
    try:
        yield
    except Exc as exc:
        if isinstance(exc, ValidationError):
            detail = json.loads(exc.json())
        else:
            detail = format_exc()
        raise HTTPException(status, detail=detail)


_handle = handle  # private alias to be used in 'validate_call'


def validate_call[F: Callable[..., Any]](
    status: int = status.HTTP_404_NOT_FOUND,
    /, *, handle: bool = True,
) -> Callable[[F], F]:
    if handle:
        return lambda f: _handle(ValidationError, status)(_validate_call(f))
    else:
        return _validate_call


__all__ = ["handle", "validate_call"]
