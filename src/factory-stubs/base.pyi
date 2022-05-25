import logging
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    List,
    Literal,
    Mapping,
    NoReturn,
    Tuple,
    Type,
    TypeVar,
    overload,
)
from typing_extensions import TypeAlias

from . import builder, declarations, errors

T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")
_Strategy: TypeAlias = Literal["build", "create", "stub"]

logger: logging.Logger

def get_factory_bases(bases: Iterable[Type[Any]]) -> List[Type[BaseFactory[Any]]]: ...
def resolve_attribute(
    name: str, bases: Iterable[Any], default: Any | None = ...
) -> Any: ...

# TODO: Add a MetaProtocol, and use for `FactoryOptions.contribute_to_class... meta`


class FactoryMetaClass(Generic[T], type):
    def __call__(cls, **kwargs: Any) -> StubObject | T: ...  # type: ignore
    def __new__(
        mcs, class_name: str, bases: Tuple[type], attrs: dict[str, Any]
    ) -> type: ...

class BaseMeta:
    abstract: bool
    strategy: _Strategy

class OptionDefault(Generic[T]):
    name: str
    value: T
    inherit: bool
    checker: Callable[[Type[Any], Any], Any]
    def __init__(
        self,
        name: str,
        value: T,
        inherit: bool = ...,
        checker: Callable[[Type[Any], Any], Any] | None = ...,
    ) -> None: ...
    def apply(self, meta: Type[Any], base_meta: FactoryOptions) -> T: ...

# Workaround for mypy until it supports typing.Self
TFactoryOptions = TypeVar("TFactoryOptions", bound=FactoryOptions)

class FactoryOptions(Generic[T]):
    factory: Type[Factory[T]] | None
    base_factory: Type[BaseFactory] | None
    base_declarations: dict[str, Any]
    parameters: dict[str, declarations.Parameter]
    parameters_dependencies: dict[str, Any]
    pre_declarations: builder.DeclarationSet
    post_declarations: builder.DeclarationSet
    counter_reference: TFactoryOptions[T] | None

    def __init__(self) -> None: ...
    @property
    def declarations(self) -> dict[str, Any]: ...
    def contribute_to_class(
        self,
        factory: Type[Factory[T]],
        meta: Type | None = ...,
        base_meta: Any | None = ...,
        base_factory: Type[BaseFactory] | None = ...,
        params: Mapping[str, Any] | None = ...,
    ): ...
    def next_sequence(self) -> int: ...
    def reset_sequence(self, value: int | None = ..., force: bool = ...) -> None: ...
    def prepare_arguments(
        self, attributes: Mapping[str, Any]
    ) -> Tuple[Tuple[Any, ...], dict[str, Any]]: ...
    def instantiate(
        self, step: builder.BuildStep, args: Type[Any], kwargs: Mapping[str, Any]
    ) -> T | StubObject: ...
    def use_postgeneration_results(
        self, step: builder.BuildStep, instance: T | StubObject, results: dict[str, Any]
    ) -> None: ...
    def get_model_class(self) -> Factory[T]: ...

class _Counter:
    seq: int
    def __init__(self, seq: int) -> None: ...
    def next(self) -> int: ...
    def reset(self, next_value: int = ...) -> None: ...

class BaseFactory(Generic[T]):
    UnknownStrategy: Type[errors.UnknownStrategy]
    UnsupportedStrategy: Type[errors.UnsupportedStrategy]
    _meta: FactoryOptions[T]
    def __new__(cls, *args: Any, **kwargs: Any) -> NoReturn: ...
    @classmethod
    def reset_sequence(cls, value: int | None = ..., force: bool = ...) -> None: ...
    @classmethod
    def _setup_next_sequence(cls) -> int: ...
    @classmethod
    def _adjust_kwargs(cls, **kwargs: Any) -> dict[str, Any]: ...
    @overload
    @classmethod
    def _generate(
        cls, strategy: Literal["build", "create"], params: dict[str, Any]
    ) -> T: ...
    @overload
    @classmethod
    def _generate(
        cls, strategy: Literal["stub"], params: dict[str, Any]
    ) -> StubObject: ...
    @classmethod
    def _after_postgeneration(
        cls,
        instance: T | StubObject,
        create: bool,
        results: dict[str, Any] | None = ...,
    ) -> None: ...
    @classmethod
    def _build(cls, model_class: Type[T], *args: Any, **kwargs: Any) -> T: ...
    @classmethod
    def _create(cls, model_class: Type[T], *args: Any, **kwargs: Any) -> T: ...
    @classmethod
    def build(cls, **kwargs: Any) -> T: ...
    @classmethod
    def build_batch(cls, size: int, **kwargs: Any) -> list[T]: ...
    @classmethod
    def create(cls, **kwargs: Any) -> T: ...
    @classmethod
    def create_batch(cls, size, **kwargs: Any) -> list[T]: ...
    @classmethod
    def stub(cls, **kwargs: Any) -> StubObject: ...
    @classmethod
    def stub_batch(cls, size: int, **kwargs: Any) -> list[StubObject]: ...
    @overload
    @classmethod
    def generate(cls, strategy: Literal["build", "create"], **kwargs: Any) -> T: ...
    @overload
    @classmethod
    def generate(cls, strategy: Literal["stub"], **kwargs: Any) -> StubObject: ...
    @overload
    @classmethod
    def generate_batch(
        cls, strategy: Literal["build", "create"], size: int, **kwargs: Any
    ) -> list[T]: ...
    @overload
    @classmethod
    def generate_batch(
        cls, strategy: Literal["stub"], size: int, **kwargs: Any
    ) -> list[StubObject]: ...
    @classmethod
    def simple_generate(cls, create: bool, **kwargs: Any) -> T: ...
    @classmethod
    def simple_generate_batch(
        cls, create: bool, size: int, **kwargs: Any
    ) -> list[T]: ...

class Factory(Generic[T], BaseFactory, metaclass=FactoryMetaClass):
    AssociatedClassError: Type[errors.AssociatedClassError]

    class Meta(BaseMeta): ...

class StubObject:
    def __init__(self, **kwargs: Any) -> None: ...

TStubObject = TypeVar("TStubObject", bound=StubObject)

class StubFactory(Factory):
    class Meta:
        strategy: Literal["stub"]
        model: Type[StubObject]
    @classmethod
    def build(cls, **kwargs: Any) -> TStubObject: ...
    @classmethod
    def create(cls, **kwargs: Any) -> NoReturn: ...

class BaseDictFactory(Generic[T], Factory[T]):
    class Meta:
        abstract: bool
    @classmethod
    def _build(cls, model_class: Type[T], **kwargs: Any) -> T: ...
    @classmethod
    def _create(cls, model_class: Type[T], **kwargs: Any) -> T: ...

class DictFactory(Generic[KT, VT], BaseDictFactory[dict[KT, VT]]):
    class Meta:
        model: Type[dict[KT, VT]]

class BaseListFactory(Generic[T], Factory[Iterable[T]]):
    class Meta:
        abstract: bool
    @classmethod
    def _build(cls, model_class: Type[Iterable[T]], **kwargs: T) -> Iterable[T]: ...

class ListFactory(Generic[T], BaseListFactory[T]):
    class Meta:
        model: list[T]

TBaseFactoryType = TypeVar("TBaseFactoryType", bound=Type[BaseFactory])

def use_strategy(
    new_strategy: _Strategy,
) -> Callable[[TBaseFactoryType], Type[TBaseFactoryType]]: ...
