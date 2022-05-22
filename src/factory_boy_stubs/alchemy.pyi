from _typeshed import Incomplete

from . import base, errors

SESSION_PERSISTENCE_COMMIT: str
SESSION_PERSISTENCE_FLUSH: str
VALID_SESSION_PERSISTENCE_TYPES: Incomplete

class SQLAlchemyOptions(base.FactoryOptions): ...

class SQLAlchemyModelFactory(base.Factory):
    class Meta:
        abstract: bool
