import dill

from .fit import Fit

__all__ = ("dumps", "loads")


def dumps(fit: Fit) -> str:
    ...


def loads(s: str) -> Fit:
    ...
