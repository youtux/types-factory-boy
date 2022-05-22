from _typeshed import Incomplete

from . import base as base
from . import declarations as declarations
from . import errors as errors

logger: Incomplete
DEFAULT_DB_ALIAS: str

def get_model(app, model): ...

class DjangoOptions(base.FactoryOptions):
    model: Incomplete
    def get_model_class(self): ...

class DjangoModelFactory(base.Factory):
    class Meta:
        abstract: bool

class FileField(declarations.BaseDeclaration):
    DEFAULT_FILENAME: str
    def evaluate(self, instance, step, extra): ...

class ImageField(FileField):
    DEFAULT_FILENAME: str

class mute_signals:
    signals: Incomplete
    paused: Incomplete
    def __init__(self, *signals) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type, exc_value, traceback) -> None: ...
    def copy(self): ...
    def __call__(self, callable_obj): ...
    def wrap_method(self, method): ...
