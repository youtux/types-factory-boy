import sys
from typing import Any, Iterable, Iterator, Literal, Mapping, NamedTuple, TypeAlias

from . import base, enums

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

StrategyType: TypeAlias = Literal["build", "create", "stub"]

class DeclarationWithContext(NamedTuple):
    name: str
    declaration: Any
    context: dict[str, Any]

class DeclarationSet:
    declarations: dict[str, Any]
    contexts: dict[str, dict[str, Any]]
    def __init__(self, initial: Mapping[str, Any] | None = ...) -> None: ...
    @classmethod
    def split(cls, entry: str) -> tuple[str, str | None]: ...
    @classmethod
    def join(cls, root: str, subkey: str | None) -> str: ...
    def copy(self) -> Self: ...
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

class BuildStep:
    builder: StepBuilder
    sequence: int
    attributes: dict[str, Any]
    parent_step: Self
    stub: Resolver
    def __init__(
        self, builder: StepBuilder, sequence: int, parent_step: Self | None = ...
    ) -> None: ...
    def resolve(self, declarations: DeclarationSet) -> None: ...
    @property
    def chain(self) -> tuple[Resolver, ...]: ...
    def recurse(
        self,
        factory: base.BaseFactory,
        declarations: DeclarationSet,
        force_sequence: int | None = ...,
    ): ...

class StepBuilder:
    factory_meta: base.FactoryOptions
    strategy: StrategyType
    extras: dict[str, Any]
    force_init_sequence: int | None
    def __init__(
        self,
        factory_meta: base.FactoryOptions,
        extras: dict[str, Any],
        strategy: StrategyType,
    ) -> None: ...
    def build(
        self,
        parent_step: BuildStep | None = ...,
        force_sequence: int | None = ...,
    ): ...
    def recurse(
        self, factory_meta: base.FactoryOptions, extras: dict[str, Any]
    ) -> Self: ...

class Resolver:
    def __init__(
        self, declarations: DeclarationSet, step: BuildStep, sequence: Any
    ) -> None: ...
    @property
    def factory_parent(self) -> Resolver: ...
    def __getattr__(self, name: Any) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
