from typing import Any

from typing_extensions import Literal

BUILD_STRATEGY: Literal["build"]
CREATE_STRATEGY: Literal["create"]
STUB_STRATEGY: Literal["stub"]
SPLITTER: str

class BuilderPhase:
    ATTRIBUTE_RESOLUTION: Literal["attributes"]
    POST_INSTANTIATION: Literal["post_instance"]

def get_builder_phase(obj: Any) -> Literal["attributes", "post_instance"] | None: ...
