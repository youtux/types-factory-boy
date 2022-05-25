import datetime
import decimal
from typing import Any, Callable, Generic, Iterable, Sequence, TypeVar

from . import declarations

T = TypeVar("T")
V = TypeVar("V")

class BaseFuzzyAttribute(declarations.BaseDeclaration):
    def fuzz(self) -> Any: ...

class FuzzyAttribute(Generic[T], BaseFuzzyAttribute):
    fuzzer: Callable[[], T]
    def __init__(self, fuzzer: Callable[[], T]) -> None: ...
    def fuzz(self) -> T: ...

class FuzzyText(BaseFuzzyAttribute):
    prefix: str
    suffix: str
    length: int
    chars: Sequence[str]
    def __init__(
        self,
        prefix: str = ...,
        length: int = ...,
        suffix: str = ...,
        chars: Iterable[str] = ...,
    ) -> None: ...
    def fuzz(self) -> str: ...

class FuzzyChoice(Generic[T, V], BaseFuzzyAttribute):
    choices: list[T] | None
    choices_generator: Iterable[T]
    getter: Callable[[T], V] | None
    def __init__(
        self, choices: Iterable[T], getter: Callable[[T], V] | None = ...
    ) -> None: ...
    def fuzz(self) -> V: ...

class FuzzyInteger(BaseFuzzyAttribute):
    low: int
    high: int
    step: int
    def __init__(self, low: int, high: int | None = ..., step: int = ...) -> None: ...
    def fuzz(self) -> int: ...

class FuzzyDecimal(BaseFuzzyAttribute):
    low: float
    high: float
    precision: int
    def __init__(
        self, low: float, high: float | None = ..., precision: int = ...
    ) -> None: ...
    def fuzz(self) -> decimal.Decimal: ...

class FuzzyFloat(BaseFuzzyAttribute):
    low: float
    high: float
    precision: int
    def __init__(
        self, low: float, high: float | None = ..., precision: int = ...
    ) -> None: ...
    def fuzz(self) -> float: ...

class FuzzyDate(BaseFuzzyAttribute):
    start_date: int
    end_date: int
    def __init__(
        self, start_date: datetime.date, end_date: datetime.date | None = ...
    ) -> None: ...
    def fuzz(self) -> datetime.date: ...

class BaseFuzzyDateTime(BaseFuzzyAttribute):
    start_dt: datetime.datetime
    end_dt: datetime.datetime
    force_year: int | None
    force_month: int | None
    force_day: int | None
    force_hour: int | None
    force_minute: int | None
    force_second: int | None
    force_microsecond: int | None
    def __init__(
        self,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime | None = ...,
        force_year: int | None = ...,
        force_month: int | None = ...,
        force_day: int | None = ...,
        force_hour: int | None = ...,
        force_minute: int | None = ...,
        force_second: int | None = ...,
        force_microsecond: int | None = ...,
    ) -> None: ...
    def fuzz(self) -> datetime.datetime: ...

class FuzzyNaiveDateTime(BaseFuzzyDateTime): ...
class FuzzyDateTime(BaseFuzzyDateTime): ...
