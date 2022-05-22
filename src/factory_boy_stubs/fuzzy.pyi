from . import declarations as declarations, random as random
from _typeshed import Incomplete

random_seed_warning: str

class BaseFuzzyAttribute(declarations.BaseDeclaration):
    def fuzz(self) -> None: ...
    def evaluate(self, instance, step, extra): ...

class FuzzyAttribute(BaseFuzzyAttribute):
    fuzzer: Incomplete
    def __init__(self, fuzzer) -> None: ...
    def fuzz(self): ...

class FuzzyText(BaseFuzzyAttribute):
    prefix: Incomplete
    suffix: Incomplete
    length: Incomplete
    chars: Incomplete
    def __init__(self, prefix: str = ..., length: int = ..., suffix: str = ..., chars=...) -> None: ...
    def fuzz(self): ...

class FuzzyChoice(BaseFuzzyAttribute):
    choices: Incomplete
    choices_generator: Incomplete
    getter: Incomplete
    def __init__(self, choices, getter: Incomplete | None = ...) -> None: ...
    def fuzz(self): ...

class FuzzyInteger(BaseFuzzyAttribute):
    low: Incomplete
    high: Incomplete
    step: Incomplete
    def __init__(self, low, high: Incomplete | None = ..., step: int = ...) -> None: ...
    def fuzz(self): ...

class FuzzyDecimal(BaseFuzzyAttribute):
    low: Incomplete
    high: Incomplete
    precision: Incomplete
    def __init__(self, low, high: Incomplete | None = ..., precision: int = ...) -> None: ...
    def fuzz(self): ...

class FuzzyFloat(BaseFuzzyAttribute):
    low: Incomplete
    high: Incomplete
    precision: Incomplete
    def __init__(self, low, high: Incomplete | None = ..., precision: int = ...) -> None: ...
    def fuzz(self): ...

class FuzzyDate(BaseFuzzyAttribute):
    start_date: Incomplete
    end_date: Incomplete
    def __init__(self, start_date, end_date: Incomplete | None = ...) -> None: ...
    def fuzz(self): ...

class BaseFuzzyDateTime(BaseFuzzyAttribute):
    start_dt: Incomplete
    end_dt: Incomplete
    force_year: Incomplete
    force_month: Incomplete
    force_day: Incomplete
    force_hour: Incomplete
    force_minute: Incomplete
    force_second: Incomplete
    force_microsecond: Incomplete
    def __init__(self, start_dt, end_dt: Incomplete | None = ..., force_year: Incomplete | None = ..., force_month: Incomplete | None = ..., force_day: Incomplete | None = ..., force_hour: Incomplete | None = ..., force_minute: Incomplete | None = ..., force_second: Incomplete | None = ..., force_microsecond: Incomplete | None = ...) -> None: ...
    def fuzz(self): ...

class FuzzyNaiveDateTime(BaseFuzzyDateTime): ...
class FuzzyDateTime(BaseFuzzyDateTime): ...
