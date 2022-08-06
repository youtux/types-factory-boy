from typing import Any, Generic, Iterable, Iterator, Mapping, NamedTuple, TypeVar

from typing_extensions import Literal, TypeAlias

from . import base

T = TypeVar("T")
V = TypeVar("V")

_Strategy: TypeAlias = Literal["build", "create", "stub"]

class DeclarationWithContext(NamedTuple):
    name: str
    declaration: Any
    context: dict[str, Any]

TDeclarationSet = TypeVar("TDeclarationSet", bound=DeclarationSet)

class DeclarationSet:
    declarations: dict[str, Any]
    contexts: dict[str, dict[str, Any]]
    def __init__(self, initial: Mapping[str, Any] | None = ...) -> None: ...
    @classmethod
    def split(cls, entry: str) -> tuple[str, str | None]: ...
    @classmethod
    def join(cls, root: str, subkey: str | None) -> str: ...
    def copy(self) -> TDeclarationSet: ...
    def update(self, values: Mapping[str, Any]) -> None: ...
    def filter(self, entries: Iterable[str]) -> list[str]: ...
    def sorted(self) -> list[str]: ...
    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str) -> DeclarationWithContext: ...
    def __iter__(self) -> Iterator[str]: ...
    def values(self) -> Iterable[DeclarationWithContext]: ...
    def as_dict(self) -> dict[str, Any]: ...

def parse_declarations(
    decls: Mapping[str, Any],
    base_pre: DeclarationSet | None = ...,
    base_post: DeclarationSet | None = ...,
) -> tuple[DeclarationSet, DeclarationSet]: ...

class BuildStep(Generic[T]):
    builder: StepBuilder[T]
    sequence: int
    attributes: dict[str, Any]
    parent_step: BuildStep[Any]
    stub: Resolver[T]
    def __init__(
        self,
        builder: StepBuilder[T],
        sequence: int,
        parent_step: BuildStep[Any] | None = ...,
    ) -> None: ...
    def resolve(self, declarations: DeclarationSet) -> None: ...
    @property
    def chain(self) -> tuple[Resolver[Any], ...]: ...
    def recurse(
        self,
        factory: base.BaseFactory[V],
        declarations: DeclarationSet,
        force_sequence: int | None = ...,
    ) -> V | base.StubObject: ...

class StepBuilder(Generic[T]):
    factory_meta: base.FactoryOptions[T]
    strategy: _Strategy
    extras: dict[str, Any]
    force_init_sequence: int | None
    def __init__(
        self,
        factory_meta: base.FactoryOptions[T],
        extras: dict[str, Any],
        strategy: _Strategy,
    ) -> None: ...
    def build(
        self,
        parent_step: BuildStep[Any] | None = ...,
        force_sequence: int | None = ...,
    ) -> T | base.StubObject: ...
    def recurse(
        self, factory_meta: base.FactoryOptions[V], extras: dict[str, Any]
    ) -> StepBuilder[V]: ...

class Resolver(Generic[T]):
    def __init__(
        self, declarations: DeclarationSet, step: BuildStep[T], sequence: Any
    ) -> None: ...
    @property
    def factory_parent(self) -> Resolver[Any]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
