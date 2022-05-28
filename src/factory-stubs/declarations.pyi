import logging
import typing
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Literal,
    Mapping,
    NamedTuple,
    Tuple,
    Type,
    TypeVar,
)

from . import base, utils, builder

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
KT = TypeVar("KT")
VT = TypeVar("VT")

logger: logging.Logger

class BaseDeclaration(Generic[T, V], utils.OrderedBase):
    FACTORY_BUILDER_PHASE: Literal["attributes", "post_instance"]
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    def __init__(self, **defaults: Any) -> None: ...
    def unroll_context(
        self,
        instance: builder.Resolver,
        step: builder.BuildStep[T],
        context: Mapping[str, Any],
    ) -> dict[str, Any]: ...
    def evaluate_pre(
        self,
        instance: builder.Resolver,
        step: builder.BuildStep[T],
        overrides: dict[str, Any],
    ) -> V: ...
    def evaluate(
        self,
        instance: builder.Resolver,
        step: builder.BuildStep[T],
        extra: dict[str, Any],
    ) -> V: ...

class OrderedDeclaration(BaseDeclaration[T, V]): ...

class LazyFunction(BaseDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    #     function: Callable[[], V]
    @staticmethod
    def function() -> V : ...
    def __init__(self, function: Callable[[], V]) -> None: ...

class LazyAttribute(BaseDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    #     function: Callable[[builder.Resolver], V]
    @staticmethod
    def function(obj: builder.Resolver, /) -> V: ...
    def __init__(self, function: Callable[[builder.Resolver], V]) -> None: ...

# TODO: Make sure that reveal_type(a) == LazyAttribute(dict[str, str], float:
# def floatify(o: dict[str, str]) -> float:
#     return float(o['asd'])
# a = LazyAttribute(floatify)
# reveal_type(a)

class _UNSPECIFIED: ...

def deepgetattr(obj: Any, name: str, default: _UNSPECIFIED | Any = ...) -> Any: ...

class SelfAttribute(BaseDeclaration[T, V]):
    depth: int
    attribute_name: str
    default: _UNSPECIFIED | Any
    def __init__(
        self, attribute_name: str, default: _UNSPECIFIED | Any = ...
    ) -> None: ...

class Iterator(Generic[U, T, V], BaseDeclaration[T, V]):
    getter: Callable[[U], V] | None
    iterator: utils.ResetableIterator[typing.Iterator[U]] | None
    iterator_builder: Callable[[], utils.ResetableIterator[U]]
    def __init__(
        self,
        iterator: typing.Iterator[U],
        cycle: bool = ...,
        getter: Callable[[U], V] | None = ...,
    ): ...
    def reset(self) -> None: ...

class Sequence(BaseDeclaration[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[int], V]
    @staticmethod
    def function(sequence: int, /) -> V: ...

    def __init__(self, function: Callable[[int], V]) -> None: ...

class LazyAttributeSequence(Sequence[T, V]):
    # Workaround for mypy bug https://github.com/python/mypy/issues/708
    # Otherwise it would just be this:
    # function: Callable[[builder.Resolver, int], V]
    @staticmethod
    def function(instance: builder.Resolver, sequence: int, /) -> V: ...  # type: ignore[override]

    def __init__(self, function: Callable[[builder.Resolver, int], V]) -> None: ...

class ContainerAttribute(BaseDeclaration[T, V]):
    function: Callable[[builder.Resolver, Tuple[builder.Resolver, ...]], V]
    strict: bool
    def __init__(
        self,
        function: Callable[[builder.Resolver, Tuple[builder.Resolver, ...]], V],
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
    # TODO: Can evaluate(instance) be a T, or can it be only a Resolver?
    def get_factory(self) -> Type[base.Factory[V]]: ...

class Dict(Generic[T, KT, VT], SubFactory[T, base.DictFactory[KT, VT]]):
    FORCE_SEQUENCE: bool

    # TODO: I'm not 100% about the type of params
    def __init__(
        self,
        params: Mapping[KT, VT | SelfAttribute[Mapping[KT, VT], VT]],
        dict_factory: str | Type[base.DictFactory[KT, VT]] = ...,
    ) -> None: ...

class List(Generic[T, V], SubFactory[T, base.ListFactory[V]]):
    FORCE_SEQUENCE: bool
    # TODO: I'm not 100% about the type of params
    def __init__(
        self, params: Iterable[V | SelfAttribute[list[V], V]], list_factory: str | Type[base.ListFactory[V]] = ...
    ) -> None: ...

class Skip:
    def __bool__(self) -> bool: ...

SKIP: Skip

class Maybe(BaseDeclaration[T, Any]):
    decider: SelfAttribute[T, Any]
    # TODO: These should be Skip | U | BaseDeclaration[T, U]
    yes: Skip | Any
    no: Skip | Any
    def __init__(
        self,
        decider: SelfAttribute[T, Any] | str,
        yes_declaration: Skip | Any = ...,
        no_declaration: Skip | Any = ...,
    ) -> None: ...
    def evaluate_post(
        self, instance: T, step: builder.BuildStep[T], overrides: dict[str, Any]
    ) -> Any: ...
    def evaluate_pre(
        self,
        instance: builder.Resolver,
        step: builder.BuildStep[T],
        overrides: dict[str, Any],
    ) -> Any: ...

class Parameter(utils.OrderedBase):
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Any]: ...
    def get_revdeps(self, parameters: dict[str, Any]) -> list[str]: ...

# TODO: This requires more typevars, remove the Anys
class SimpleParameter(Generic[T], Parameter):
    value: T
    def __init__(self, value: T) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, T]: ...
    @classmethod
    def wrap(cls, value: utils.OrderedBase | Parameter | Any) -> utils.OrderedBase: ...

# TODO: this needs more typevars, remove the Anys
class Trait(Parameter):
    overrides: dict[str, Any]
    def __init__(self, **overrides: Any) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Maybe[Any]]: ...

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
    def function(obj: T, create: bool, extracted: Any, /, **kwargs: Any) -> V: ...
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
