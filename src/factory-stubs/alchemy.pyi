from typing import List, Optional

from . import base

SESSION_PERSISTENCE_COMMIT: str
SESSION_PERSISTENCE_FLUSH: str
VALID_SESSION_PERSISTENCE_TYPES: List[Optional[str]]

class SQLAlchemyOptions(base.FactoryOptions): ...

class SQLAlchemyModelFactory(base.Factory):
    class Meta:
        abstract: bool
