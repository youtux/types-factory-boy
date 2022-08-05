import logging
from types import TracebackType
from typing import Any, TypeVar, Type, Callable, Hashable, overload
from typing_extensions import ParamSpec

from django.db import models
from django.dispatch.dispatcher import Signal
from django.core.files import File

from . import base, declarations

T = TypeVar("T")
V = TypeVar("V")
P = ParamSpec("P")
TModel = TypeVar("TModel", bound=models.Model)

logger: logging.Logger
DEFAULT_DB_ALIAS: str

def get_model(app: str, model: str | None = ...) -> Type[models.Model]: ...

class DjangoOptions(base.FactoryOptions[TModel]):
    def get_model_class(self) -> Type[TModel]: ...

class DjangoModelFactory(base.Factory[TModel]):
    class Meta:
        abstract: bool

class FileField(declarations.BaseDeclaration[Any, File]):
    DEFAULT_FILENAME: str

class ImageField(FileField):
    DEFAULT_FILENAME: str

# Replace this with `Self` once mypy supports it
mute_signals_T = TypeVar("mute_signals_T", bound=mute_signals)

FactoryTypeT = TypeVar("FactoryTypeT", bound=Type[base.Factory[Any]])

class mute_signals:
    signals: tuple[Signal]
    paused: dict[Signal, tuple[tuple[Hashable, int], Callable[..., Any]]]
    def __init__(self, *signals: Signal) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None: ...
    def copy(self) -> mute_signals_T: ...
    @overload
    def __call__(self, callable_obj: FactoryTypeT) -> FactoryTypeT: ...
    @overload
    def __call__(self, callable_obj: Callable[P, V]) -> Callable[P, V]: ...
    # TODO: Not sure about this one
    def wrap_method(self, method: Callable[P, V]) -> Callable[P, V]: ...
