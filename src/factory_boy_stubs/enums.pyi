BUILD_STRATEGY: str
CREATE_STRATEGY: str
STUB_STRATEGY: str
SPLITTER: str

class BuilderPhase:
    ATTRIBUTE_RESOLUTION: str
    POST_INSTANTIATION: str

def get_builder_phase(obj): ...
