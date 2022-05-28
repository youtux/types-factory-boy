from typing import TypeVar

from . import base

T = TypeVar("T")

class MogoFactory(base.Factory[T]):
    class Meta:
        abstract: bool
