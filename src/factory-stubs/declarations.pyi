import logging
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

from factory.builder import BuildStep, Resolver

from . import base, utils

T = TypeVar("T")
V = TypeVar("V")
KT = TypeVar("KT")
VT = TypeVar("VT")

TFactory = TypeVar("TFactory", bound=base.Factory)

logger: logging.Logger

class BaseDeclaration(utils.OrderedBase):
    FACTORY_BUILDER_PHASE: Literal["attributes", "post_instance"]
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    def __init__(self, **defaults: Any) -> None: ...
    def unroll_context(
        self, instance: Resolver, step: BuildStep, context: Mapping[str, Any]
    ) -> dict[str, Any]: ...
    def evaluate_pre(
        self, instance: Resolver, step: BuildStep, overrides: dict[str, Any]
    ): ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> Any: ...

class OrderedDeclaration(BaseDeclaration): ...

class LazyFunction(Generic[T], BaseDeclaration):
    function: Callable[[], T]
    def __init__(self, function: Callable[[], T]) -> None: ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...

class LazyAttribute(Generic[T], BaseDeclaration):
    function: Callable[[Resolver], T]
    def __init__(self, function: Callable[[Resolver], T]) -> None: ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...

class _UNSPECIFIED: ...

def deepgetattr(obj: Any, name: str, default: _UNSPECIFIED | Any = ...) -> Any: ...

class SelfAttribute(BaseDeclaration):
    depth: int
    attribute_name: str
    default: _UNSPECIFIED | Any
    def __init__(
        self, attribute_name: str, default: _UNSPECIFIED | Any = ...
    ) -> None: ...

class Iterator(Generic[T, V], BaseDeclaration):
    getter: Callable[[T], V] | None
    iterator: utils.ResetableIterator[Iterator[T]] | None
    iterator_builder: Callable[[], utils.ResetableIterator[T]]
    def __init__(
        self,
        iterator: Iterator[T],
        cycle: bool = ...,
        getter: Callable[[T], V] | None = ...,
    ): ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...
    def reset(self) -> None: ...

class Sequence(Generic[T], BaseDeclaration):
    function: Callable[[int], T]
    def __init__(self, function: Callable[[int], T]) -> None: ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...

class LazyAttributeSequence(Sequence[T]):
    function: Callable[[Resolver, int], T]
    def __init__(self, function: Callable[[Resolver, int], T]) -> None: ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...

class ContainerAttribute(Generic[T], BaseDeclaration):
    function: Callable[[Resolver, Tuple[Resolver, ...]], T]
    strict: bool
    def __init__(
        self,
        function: Callable[[Resolver, Tuple[Resolver, ...]], T],
        strict: bool = ...,
    ) -> None: ...
    def evaluate(
        self, instance: Resolver, step: BuildStep, extra: dict[str, Any]
    ) -> T: ...

class ParameteredAttribute(BaseDeclaration):
    def generate(self, step: BuildStep, params: dict[str, Any]) -> Any: ...

class _FactoryWrapper(Generic[TFactory]):
    factory: Type[TFactory] | None
    module: str
    def __init__(self, factory_or_path: str | Type[TFactory]) -> None: ...
    def get(self) -> Type[TFactory]: ...

class SubFactory(Generic[TFactory], BaseDeclaration):
    FORCE_SEQUENCE: bool
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    factory_wrapper: _FactoryWrapper[TFactory]
    def __init__(self, factory: str | Type[TFactory], **kwargs: Any) -> None: ...
    def get_factory(self) -> Type[TFactory]: ...

class Dict(Mapping[KT, VT], SubFactory[base.DictFactory[KT, VT]]):
    FORCE_SEQUENCE: bool
    def __init__(
        self,
        params: Mapping[KT, VT] | Iterable[Tuple[KT, VT]],
        dict_factory: str | Type[base.Factory] = ...,
    ) -> None: ...

class List(Generic[T], SubFactory[base.ListFactory[T]]):
    FORCE_SEQUENCE: bool
    def __init__(
        self, params: Iterable[T], list_factory: str | Type[base.Factory] = ...
    ) -> None: ...

class Skip:
    def __bool__(self) -> bool: ...

SKIP: Skip

class Maybe(BaseDeclaration):
    decider: SelfAttribute
    yes: Any
    no: Any
    def __init__(
        self,
        decider: SelfAttribute | str,
        yes_declaration: Skip | Any = ...,
        no_declaration: Skip | Any = ...,
    ) -> None: ...
    def evaluate_post(
        self, instance: Any, step: BuildStep, overrides: dict[str, Any]
    ) -> Any: ...
    def evaluate_pre(
        self, instance: Resolver, step: BuildStep, overrides: dict[str, Any]
    ) -> Any: ...

class Parameter(utils.OrderedBase):
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Any]: ...
    def get_revdeps(self, parameters: dict[str, Any]) -> list[str]: ...

class SimpleParameter(Generic[T], Parameter):
    value: T
    def __init__(self, value: T) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, T]: ...
    @classmethod
    def wrap(cls, value: utils.OrderedBase | Parameter | Any) -> utils.OrderedBase: ...

class Trait(Parameter):
    overrides: dict[str, Any]
    def __init__(self, **overrides: Any) -> None: ...
    def as_declarations(
        self, field_name: str, declarations: dict[str, Any]
    ) -> dict[str, Maybe]: ...

class PostGenerationContext(NamedTuple):
    value_provided: bool
    value: Any
    extra: dict[str, Any]

class PostGenerationDeclaration(BaseDeclaration):
    def evaluate_post(
        self, instance: Any, step: BuildStep, overrides: dict[str, Any]
    ) -> Any: ...
    def call(
        self, instance: Any, step: BuildStep, context: PostGenerationContext
    ) -> Any: ...

class PostGeneration(PostGenerationDeclaration):
    function: Callable[[Any, bool, Any, ...], Any]
    def __init__(self, function: Callable[[Any, bool, Any, ...], Any]) -> None: ...
    def call(
        self, instance: Any, step: BuildStep, context: PostGenerationContext
    ) -> Any: ...

class RelatedFactory(Generic[TFactory], PostGenerationDeclaration):
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    name: str
    defaults: dict[str, Any]
    factory_wrapper: _FactoryWrapper[TFactory]
    def __init__(
        self,
        factory: str | Type[TFactory],
        factory_related_name: str = ...,
        **defaults: Any,
    ) -> None: ...
    def get_factory(self) -> Type[TFactory]: ...

class RelatedFactoryList(Generic[TFactory], RelatedFactory[TFactory]):
    size: int | Callable[[], int]
    def __init__(
        self,
        factory: str | Type[TFactory],
        factory_related_name: str = ...,
        size: int | Callable[[], int] = ...,
        **defaults: Any,
    ) -> None: ...
    def call(
        self, instance: Any, step: BuildStep, context: PostGenerationContext
    ) -> list[Any]: ...

class NotProvided: ...

class PostGenerationMethodCall(PostGenerationDeclaration):
    method_name: str
    method_arg: Any
    method_kwargs: dict[str, Any]
    def __init__(self, method_name: str, *args: Any, **kwargs: Any) -> None: ...
