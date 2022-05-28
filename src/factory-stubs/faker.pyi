from typing import Any, ContextManager, TypeVar, Generic

import faker
import faker.providers

from . import declarations

T = TypeVar("T")  # Type of the instance
V = TypeVar("V")  # Type of the attribute

class Faker(Generic[T, V], declarations.BaseDeclaration[T, V]):
    provider: str
    def __init__(self, provider: str, **kwargs: declarations.BaseDeclaration[T, Any] | Any) -> None: ...
    @classmethod
    def override_default_locale(cls, locale: str) -> ContextManager[None]: ...
    @classmethod
    @classmethod
    def _get_faker(cls, locale: str | None = ...) -> faker.Faker: ...
    @classmethod
    def add_provider(
        cls, provider: faker.providers.BaseProvider, locale: str | None = ...
    ) -> None: ...
