from typing import (
    Any,
    Callable,
    ContextManager,
    Iterator,
    Literal,
    TextIO,
    Type,
    TypeVar,
    overload,
)

T = TypeVar("T")  # Type of the instance
V = TypeVar("V")  # Type of the attribute

from . import base, builder, declarations

def debug(logger: str = ..., stream: TextIO | None = ...) -> ContextManager[None]: ...
def make_factory(klass: T, **kwargs: Any) -> Type[base.Factory[T]]: ...
def build(klass: T, **kwargs: Any) -> T: ...
def build_batch(klass: T, size: int, **kwargs: Any) -> list[T]: ...
def create(klass: T, **kwargs: Any) -> T: ...
def create_batch(klass: T, size: int, **kwargs: Any) -> list[T]: ...
def stub(klass: T, **kwargs: Any) -> base.StubObject: ...
def stub_batch(klass: T, size: int, **kwargs: Any) -> base.StubObject: ...
@overload
def generate(klass: T, strategy: Literal["build", "create"], **kwargs: Any) -> T: ...
@overload
def generate(klass: T, strategy: Literal["stub"], **kwargs: Any) -> base.StubObject: ...
@overload
def generate_batch(
    klass: T, strategy: Literal["build", "create"], size: int, **kwargs: Any
) -> list[T]: ...
@overload
def generate_batch(
    klass: T, strategy: Literal["stub"], size: int, **kwargs: Any
) -> list[base.StubObject]: ...
def simple_generate(klass: T, create: bool, **kwargs: Any) -> T: ...
def simple_generate_batch(
    klass: T, create: bool, size: int, **kwargs: Any
) -> list[T]: ...
def lazy_attribute(
    func: Callable[[builder.Resolver], V]
) -> declarations.LazyAttribute[Any, V]: ...
def iterator(func: Callable[[], Iterator[V]]) -> declarations.Iterator[V, V]: ...
def sequence(func: Callable[[int], V]) -> declarations.Sequence[V]: ...
def lazy_attribute_sequence(
    func: Callable[[builder.Resolver, int], V]
) -> declarations.LazyAttributeSequence[T, V]: ...
def container_attribute(
    func: Callable[[builder.Resolver, tuple[builder.Resolver, ...]], V]
) -> declarations.ContainerAttribute[T, V]: ...
def post_generation(
    fun: Callable[[T, bool, Any], V]
) -> declarations.PostGeneration[T, V]: ...
