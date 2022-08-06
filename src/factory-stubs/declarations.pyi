import logging
import typing
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Mapping,
    NamedTuple,
    Tuple,
    Type,
    TypeVar,
)

from typing_extensions import Literal

from . import base, builder, utils

T = TypeVar("T")  # Type of the instance
V = TypeVar("V")  # Type of the attribute
S = TypeVar("S")  # General purpose type

KT = TypeVar("KT")
VT = TypeVar("VT")

logger: logging.Logger

class BaseDeclaration(Generic[T, V], utils.OrderedBase):
    FACTORY_BUILDER_PHASE: Literal["attributes", "post_instance"]
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    def __init__(self, **defaults: Any) -> None: ...
    def unroll_context(
        self,
        instance: builder.Resolver[T],
        step: builder.BuildStep[T],
        context: Mapping[str, Any],
    ) -> dict[str, Any]: ...
    def evaluate_pre(
        self,
        instance: builder.Resolver[T],
        step: builder.BuildStep[T],
        overrides: dict[str, Any],
    ) -> V: ...
    def evaluate(
        self,
        instance: builder.Resolver[T],
        step: builder.BuildStep[T],
        extra: dict[str, Any],
    ) -> V: ...

class OrderedDeclaration(BaseDeclaration[T, V]): ...

class LazyFunction(BaseDeclaration[Any, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    #     function: Callable[[], V]
    @staticmethod
    def function() -> V: ...
    def __init__(self, function: Callable[[], V]) -> None: ...

class LazyAttribute(BaseDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    #     function: Callable[[builder.Resolver], V]
    @staticmethod
    def function(__obj: builder.Resolver[T]) -> V: ...
    def __init__(self, function: Callable[[builder.Resolver[T]], V]) -> None: ...

class _UNSPECIFIED: ...

def deepgetattr(obj: Any, name: str, default: _UNSPECIFIED | Any = ...) -> Any: ...

# TODO: Not sure if SelfAttribute can have T type, since it can access parents. Check that.
class SelfAttribute(BaseDeclaration[T, V]):
    depth: int
    attribute_name: str
    default: _UNSPECIFIED | Any
    def __init__(
        self, attribute_name: str, default: _UNSPECIFIED | Any = ...
    ) -> None: ...

class Iterator(Generic[S, V], BaseDeclaration[Any, V]):
    getter: Callable[[S], V] | None
    iterator: utils.ResetableIterator[S] | None
    iterator_builder: Callable[[], utils.ResetableIterator[S]]
    def __init__(
        self,
        iterator: typing.Iterable[T],
        cycle: bool = ...,
        getter: Callable[[T], V] | None = ...,
    ): ...
    def reset(self) -> None: ...

class Sequence(BaseDeclaration[Any, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[int], V]
    @staticmethod
    def function(__sequence: int) -> V: ...
    def __init__(self, function: Callable[[int], V]) -> None: ...

class LazyAttributeSequence(Generic[T, V], Sequence[V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[builder.Resolver[T], int], V]
    @staticmethod
    def function(__instance: builder.Resolver[T], __sequence: int) -> V: ...  # type: ignore[override]
    def __init__(self, function: Callable[[builder.Resolver[T], int], V]) -> None: ...

class ContainerAttribute(BaseDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[builder.Resolver[T], Tuple[builder.Resolver[Any, ...]], V]
    @staticmethod
    def function(
        __obj: builder.Resolver[T], __containers: Tuple[builder.Resolver[Any], ...]
    ) -> V: ...

    strict: bool

    def __init__(
        self,
        function: Callable[[builder.Resolver[T], Tuple[builder.Resolver[Any], ...]], V],
        strict: bool = ...,
    ) -> None: ...

class ParameteredAttribute(BaseDeclaration[T, V]):
    def generate(self, step: builder.BuildStep[T], params: dict[str, Any]) -> V: ...

class _FactoryWrapper(Generic[T]):
    factory: Type[base.Factory[T]] | None
    module: str
    def __init__(self, factory_or_path: str | Type[base.Factory[T]]) -> None: ...
    def get(self) -> Type[base.Factory[T]]: ...

class SubFactory(BaseDeclaration[T, V]):
    FORCE_SEQUENCE: bool
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    factory_wrapper: _FactoryWrapper[base.Factory[V]]
    def __init__(self, factory: str | Type[base.Factory[V]], **kwargs: Any) -> None: ...
    def get_factory(self) -> Type[base.Factory[V]]: ...

class Dict(Generic[T, KT, VT], SubFactory[T, dict[KT, VT]]):
    FORCE_SEQUENCE: bool

    # TODO: I'm not 100% about the type of params
    def __init__(
        self,
        params: Mapping[KT, VT | SelfAttribute[Mapping[KT, VT], VT]],
        dict_factory: str | Type[base.DictFactory[Mapping[KT, VT]]] = ...,
    ) -> None: ...

class List(Generic[T, V], SubFactory[T, list[V]]):
    FORCE_SEQUENCE: bool
    # TODO: I'm not 100% about the type of params
    def __init__(
        self,
        params: Iterable[V | SelfAttribute[list[V], V]],
        list_factory: str | Type[base.ListFactory[typing.Container[V]]] = ...,
    ) -> None: ...

class Skip:
    def __bool__(self) -> bool: ...

SKIP: Skip

class Maybe(BaseDeclaration[T, V]):
    decider: BaseDeclaration[T, Any]
    yes: Skip | V | BaseDeclaration[T, V]
    no: Skip | V | BaseDeclaration[T, V]
    def __init__(
        self,
        decider: BaseDeclaration[T, Any] | str,
        yes_declaration: Skip | V | BaseDeclaration[T, V] = ...,
        no_declaration: Skip | V | BaseDeclaration[T, V] = ...,
    ) -> None: ...
    def evaluate_post(
        self, instance: T, step: builder.BuildStep[T], overrides: dict[str, Any]
    ) -> V: ...
    def evaluate_pre(
        self,
        instance: builder.Resolver[T],
        step: builder.BuildStep[T],
        overrides: dict[str, Any],
    ) -> V: ...

class Parameter(utils.OrderedBase):
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Any]: ...
    def get_revdeps(self, parameters: dict[str, Any]) -> list[str]: ...

class SimpleParameter(Generic[S], Parameter):
    value: S
    def __init__(self, value: S) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, S]: ...
    @classmethod
    def wrap(cls, value: Any) -> Parameter: ...

class Trait(Generic[T], Parameter):
    overrides: dict[str, Any]
    def __init__(self, **overrides: BaseDeclaration[T, Any] | Any) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Maybe[T, Any]]: ...

class PostGenerationContext(NamedTuple):
    value_provided: bool
    value: Any
    extra: dict[str, Any]

class PostGenerationDeclaration(BaseDeclaration[T, V]):
    def evaluate_post(
        self, instance: T, step: builder.BuildStep[T], overrides: dict[str, Any]
    ) -> V: ...
    def call(
        self, instance: T, step: builder.BuildStep[T], context: PostGenerationContext
    ) -> V: ...

class PostGeneration(PostGenerationDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[T, bool, Any, ...], V]
    @staticmethod
    def function(__obj: T, __create: bool, __extracted: Any, **kwargs: Any) -> V: ...
    def __init__(self, function: Callable[[T, bool, Any], V]) -> None: ...

class RelatedFactory(PostGenerationDeclaration[T, V]):
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    name: str
    defaults: dict[str, Any]
    factory_wrapper: _FactoryWrapper[base.Factory[V]]
    def __init__(
        self,
        factory: str | Type[base.Factory[V]],
        factory_related_name: str = ...,
        **defaults: Any,
    ) -> None: ...
    def get_factory(self) -> Type[base.Factory[V]]: ...

class RelatedFactoryList(Generic[T, V], RelatedFactory[T, list[V]]):
    size: int | Callable[[], int]
    def __init__(
        self,
        factory: str | Type[base.Factory[V]],
        factory_related_name: str = ...,
        size: int | Callable[[], int] = ...,
        **defaults: Any,
    ) -> None: ...

class NotProvided: ...

class PostGenerationMethodCall(PostGenerationDeclaration[T, V]):
    method_name: str
    method_arg: Any
    method_kwargs: dict[str, Any]
    def __init__(self, method_name: str, *args: Any, **kwargs: Any) -> None: ...
