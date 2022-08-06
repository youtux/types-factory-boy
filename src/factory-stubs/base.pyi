import logging
from typing import (
    Any,
    Callable,
    Container,
    Generic,
    Iterable,
    List,
    Mapping,
    NoReturn,
    Tuple,
    Type,
    TypeVar,
    overload,
)

from typing_extensions import Literal, TypeAlias

from . import builder, declarations, errors

# TODO: Figure out if we have to use covariant types for collections
T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")
_Strategy: TypeAlias = Literal["build", "create", "stub"]

logger: logging.Logger

def get_factory_bases(bases: Iterable[Type[Any]]) -> List[Type[BaseFactory[Any]]]: ...
def resolve_attribute(
    name: str, bases: Iterable[Any], default: Any | None = ...
) -> Any: ...

class FactoryMetaClass(Generic[T], type):
    def __call__(cls, **kwargs: Any) -> StubObject | T: ...  # type: ignore[override]
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
    def apply(self, meta: Type[Any], base_meta: FactoryOptions[Any]) -> T: ...

class FactoryOptions(Generic[T]):
    factory: Type[Factory[T]] | None
    base_factory: Type[BaseFactory[Any]] | None
    base_declarations: dict[str, Any]
    parameters: dict[str, declarations.Parameter]
    parameters_dependencies: dict[str, Any]
    pre_declarations: builder.DeclarationSet
    post_declarations: builder.DeclarationSet
    counter_reference: FactoryOptions[T] | None

    def __init__(self) -> None: ...
    @property
    def declarations(self) -> dict[str, Any]: ...
    def contribute_to_class(
        self,
        factory: Type[Factory[T]],
        meta: Type[Any] | None = ...,
        base_meta: FactoryOptions[T] | None = ...,
        base_factory: Type[BaseFactory[Any]] | None = ...,
        params: Mapping[str, Any] | None = ...,
    ) -> None: ...
    def next_sequence(self) -> int: ...
    def reset_sequence(self, value: int | None = ..., force: bool = ...) -> None: ...
    def prepare_arguments(
        self, attributes: Mapping[str, Any]
    ) -> Tuple[Tuple[Any, ...], dict[str, Any]]: ...
    def instantiate(
        self, step: builder.BuildStep[T], args: Iterable[Any], kwargs: Mapping[str, Any]
    ) -> T | StubObject: ...
    def use_postgeneration_results(
        self,
        step: builder.BuildStep[T],
        instance: T | StubObject,
        results: dict[str, Any],
    ) -> None: ...
    def get_model_class(self) -> Type[T]: ...

class _Counter:
    seq: int
    def __init__(self, seq: int) -> None: ...
    def next(self) -> int: ...
    def reset(self, next_value: int = ...) -> None: ...

class BaseFactory(Generic[T]):
    UnknownStrategy: Type[errors.UnknownStrategy]
    UnsupportedStrategy: Type[errors.UnsupportedStrategy]
    _meta: FactoryOptions[T]
    def __new__(cls, *args: Any, **kwargs: Any) -> NoReturn: ...  # type: ignore
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
    def create_batch(cls, size: int, **kwargs: Any) -> list[T]: ...
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

class Factory(Generic[T], BaseFactory[T], metaclass=FactoryMetaClass):
    AssociatedClassError: Type[errors.AssociatedClassError]

    class Meta(BaseMeta): ...

class StubObject:
    def __init__(self, **kwargs: Any) -> None: ...

class StubFactory(Factory[StubObject]):
    class Meta:
        strategy: Literal["stub"]
        model: Type[StubObject]
    @classmethod
    def build(cls, **kwargs: Any) -> StubObject: ...
    @classmethod
    def create(cls, **kwargs: Any) -> NoReturn: ...

TMapping = TypeVar("TMapping", bound=Mapping[Any, Any])

class BaseDictFactory(Factory[TMapping]):
    class Meta:
        abstract: bool

class DictFactory(BaseDictFactory[TMapping]):
    class Meta:
        # This would be:
        # model: Type[TMapping]
        # but mypy doesn't support it
        model: Type[dict[Any, Any]]

TContainer = TypeVar("TContainer", bound=Container[Any])

class BaseListFactory(Factory[TContainer]):
    class Meta:
        abstract: bool

class ListFactory(BaseListFactory[TContainer]):
    class Meta:
        # This would be:
        # model: Type[TContainer]
        # but mypy doesn't support it
        model: Type[list[Any]]

TBaseFactoryType = TypeVar("TBaseFactoryType", bound=Type[BaseFactory[Any]])

def use_strategy(
    new_strategy: _Strategy,
) -> Callable[[TBaseFactoryType], Type[TBaseFactoryType]]: ...
