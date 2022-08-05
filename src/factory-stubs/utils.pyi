import collections
from types import ModuleType
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
)

T = TypeVar("T")

def import_object(module_name: str, attribute_name: str) -> ModuleType: ...

class log_pprint:
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
    def __init__(
        self, args: Sequence[Any] = ..., kwargs: Optional[Mapping[str, Any]] = ...
    ) -> None: ...

class ResetableIterator(Generic[T]):
    iterator: Iterator[T]
    past_elements: collections.deque[T]
    next_elements: collections.deque[T]
    def __init__(self, iterator: Iterable[T], **kwargs: Any) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
    def reset(self) -> None: ...

class OrderedBase:
    CREATION_COUNTER_FIELD: str
    def __init__(self, **kwargs: Any) -> None: ...
    def touch_creation_counter(self) -> None: ...

def sort_ordered_objects(
    items: Iterable[T], getter: Optional[Callable[[T], OrderedBase]] = ...
) -> List[T]: ...
