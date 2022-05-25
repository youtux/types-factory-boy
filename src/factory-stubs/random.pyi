import random
import sys
from typing import Any

randgen: random.Random

def get_random_state() -> tuple[Any, ...]: ...
def set_random_state(state: tuple[Any, ...]) -> None: ...

# Using other `seed` types is deprecated since 3.9 and removed in 3.11
if sys.version_info >= (3, 9):
    def reseed_random(seed: int | float | str | bytes | bytearray | None) -> None: ...

else:
    def reseed_random(seed: Any) -> None: ...
