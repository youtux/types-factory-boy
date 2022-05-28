from typing import List, Optional, TypeVar

from . import base

T = TypeVar("T")

SESSION_PERSISTENCE_COMMIT: str
SESSION_PERSISTENCE_FLUSH: str
VALID_SESSION_PERSISTENCE_TYPES: List[Optional[str]]

class SQLAlchemyOptions(base.FactoryOptions[T]): ...

class SQLAlchemyModelFactory(base.Factory[T]):
    class Meta:
        abstract: bool
