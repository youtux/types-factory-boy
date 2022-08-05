import datetime
import decimal
from typing import Any, Callable, Generic, Iterable, Sequence, TypeVar

from . import declarations

V = TypeVar("V")  # Type of the attribute
S = TypeVar("S")  # General purpose type

class BaseFuzzyAttribute(declarations.BaseDeclaration[Any, V]):
    def fuzz(self) -> V: ...

class FuzzyAttribute(BaseFuzzyAttribute[V]):
    fuzzer: Callable[[], V]
    def __init__(self, fuzzer: Callable[[], V]) -> None: ...

class FuzzyText(BaseFuzzyAttribute[str]):
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

class FuzzyChoice(Generic[S, V], BaseFuzzyAttribute[V]):
    choices: list[S] | None
    choices_generator: Iterable[S]
    getter: Callable[[S], V] | None
    def __init__(
        self, choices: Iterable[S], getter: Callable[[S], V] | None = ...
    ) -> None: ...

class FuzzyInteger(BaseFuzzyAttribute[int]):
    low: int
    high: int
    step: int
    def __init__(self, low: int, high: int | None = ..., step: int = ...) -> None: ...

class FuzzyDecimal(BaseFuzzyAttribute[decimal.Decimal]):
    low: float
    high: float
    precision: int
    def __init__(
        self, low: float, high: float | None = ..., precision: int = ...
    ) -> None: ...

class FuzzyFloat(BaseFuzzyAttribute[float]):
    low: float
    high: float
    precision: int
    def __init__(
        self, low: float, high: float | None = ..., precision: int = ...
    ) -> None: ...

class FuzzyDate(BaseFuzzyAttribute[datetime.date]):
    start_date: int
    end_date: int
    def __init__(
        self, start_date: datetime.date, end_date: datetime.date | None = ...
    ) -> None: ...

class BaseFuzzyDateTime(BaseFuzzyAttribute[datetime.datetime]):
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

class FuzzyNaiveDateTime(BaseFuzzyDateTime): ...
class FuzzyDateTime(BaseFuzzyDateTime): ...
