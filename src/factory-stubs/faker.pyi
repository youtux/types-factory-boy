from typing import Any, ContextManager

import faker
import faker.providers

from . import declarations

class Faker(declarations.BaseDeclaration):
    provider: str
    def __init__(self, provider: str, **kwargs: Any) -> None: ...
    @classmethod
    def override_default_locale(cls, locale: str) -> ContextManager[None]: ...
    @classmethod
    @classmethod
    def _get_faker(cls, locale: str | None = ...) -> faker.Faker: ...
    @classmethod
    def add_provider(
        cls, provider: faker.providers.BaseProvider, locale: str | None = ...
    ) -> None: ...
