from typing import TypeVar

from . import base

T = TypeVar("T")

class MongoEngineFactory(base.Factory[T]):
    class Meta:
        abstract: bool
