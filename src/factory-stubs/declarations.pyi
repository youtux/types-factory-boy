import logging
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Literal,
    Mapping,
    Tuple,
    Type,
    TypeVar,
)

from _typeshed import Incomplete
from factory.builder import BuildStep, Resolver

from . import base, utils

T = TypeVar("T")
V = TypeVar("V")
KT = TypeVar("KT")
VT = TypeVar("VT")

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

class _FactoryWrapper:
    factory: Type[base.Factory] | None
    module: str
    def __init__(self, factory_or_path: str | Type[base.Factory]) -> None: ...
    def get(self) -> Type[base.Factory]: ...

class SubFactory(BaseDeclaration):
    FORCE_SEQUENCE: bool
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    factory_wrapper: _FactoryWrapper
    def __init__(self, factory: str | Type[base.Factory], **kwargs: Any) -> None: ...
    def get_factory(self) -> Type[base.Factory]: ...

class Dict(Mapping[KT, VT], SubFactory):
    FORCE_SEQUENCE: bool
    def __init__(
        self,
        params: Mapping[KT, VT] | Iterable[Tuple[KT, VT]],
        dict_factory: str | Type[base.Factory] = ...,
    ) -> None: ...

class List(Generic[T], SubFactory):
    FORCE_SEQUENCE: bool
    def __init__(
        self, params: Iterable[T], list_factory: str | Type[base.Factory] = ...
    ) -> None: ...

class Skip:
    def __bool__(self) -> bool: ...

SKIP: Skip

class Maybe(BaseDeclaration):
    decider: SelfAttribute
    yes: Incomplete
    no: Incomplete
    FACTORY_BUILDER_PHASE: Incomplete
    def __init__(
        self,
        decider: SelfAttribute | str,
        yes_declaration: Skip | Any = ...,
        no_declaration: Skip | Any = ...,
    ) -> None: ...
    def evaluate_post(
        self, instance: Resolver, step: BuildStep, overrides: dict[str, Any]
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

# TODO: CONTINUE FROM HERE

class Trait(Parameter):
    overrides: Incomplete
    def __init__(self, **overrides) -> None: ...
    def as_declarations(self, field_name, declarations): ...
    def get_revdeps(self, parameters): ...

class PostGenerationContext(T.NamedTuple):
    value_provided: bool
    value: T.Any
    extra: T.Dict[str, T.Any]

class PostGenerationDeclaration(BaseDeclaration):
    FACTORY_BUILDER_PHASE: Incomplete
    def evaluate_post(self, instance, step, overrides): ...
    def call(self, instance, step, context) -> None: ...

class PostGeneration(PostGenerationDeclaration):
    function: Incomplete
    def __init__(self, function) -> None: ...
    def call(self, instance, step, context): ...

class RelatedFactory(PostGenerationDeclaration):
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool
    name: Incomplete
    defaults: Incomplete
    factory_wrapper: Incomplete
    def __init__(
        self, factory, factory_related_name: str = ..., **defaults
    ) -> None: ...
    def get_factory(self): ...
    def call(self, instance, step, context): ...

class RelatedFactoryList(RelatedFactory):
    size: Incomplete
    def __init__(
        self, factory, factory_related_name: str = ..., size: int = ..., **defaults
    ) -> None: ...
    def call(self, instance, step, context): ...

class NotProvided: ...

class PostGenerationMethodCall(PostGenerationDeclaration):
    method_name: Incomplete
    method_arg: Incomplete
    method_kwargs: Incomplete
    def __init__(self, method_name, *args, **kwargs) -> None: ...
    def call(self, instance, step, context): ...
