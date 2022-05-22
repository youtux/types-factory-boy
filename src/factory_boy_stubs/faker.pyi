from collections.abc import Generator

from _typeshed import Incomplete

from . import declarations

class Faker(declarations.BaseDeclaration):
    provider: Incomplete
    def __init__(self, provider, **kwargs) -> None: ...
    def evaluate(self, instance, step, extra): ...
    @classmethod
    def override_default_locale(cls, locale) -> Generator[None, None, None]: ...
    @classmethod
    def add_provider(cls, provider, locale: Incomplete | None = ...) -> None: ...
