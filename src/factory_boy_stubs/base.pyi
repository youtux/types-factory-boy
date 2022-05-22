from _typeshed import Incomplete

from . import builder as builder
from . import declarations as declarations
from . import enums as enums
from . import errors as errors
from . import utils as utils

logger: Incomplete

def get_factory_bases(bases): ...
def resolve_attribute(name, bases, default: Incomplete | None = ...): ...

class FactoryMetaClass(type):
    def __call__(cls, **kwargs): ...
    def __new__(mcs, class_name, bases, attrs): ...

class BaseMeta:
    abstract: bool
    strategy: Incomplete

class OptionDefault:
    name: Incomplete
    value: Incomplete
    inherit: Incomplete
    checker: Incomplete
    def __init__(
        self, name, value, inherit: bool = ..., checker: Incomplete | None = ...
    ) -> None: ...
    def apply(self, meta, base_meta): ...

class FactoryOptions:
    factory: Incomplete
    base_factory: Incomplete
    base_declarations: Incomplete
    parameters: Incomplete
    parameters_dependencies: Incomplete
    pre_declarations: Incomplete
    post_declarations: Incomplete
    counter_reference: Incomplete
    def __init__(self) -> None: ...
    @property
    def declarations(self): ...
    model: Incomplete
    abstract: bool
    def contribute_to_class(
        self,
        factory,
        meta: Incomplete | None = ...,
        base_meta: Incomplete | None = ...,
        base_factory: Incomplete | None = ...,
        params: Incomplete | None = ...,
    ): ...
    def next_sequence(self): ...
    def reset_sequence(
        self, value: Incomplete | None = ..., force: bool = ...
    ) -> None: ...
    def prepare_arguments(self, attributes): ...
    def instantiate(self, step, args, kwargs): ...
    def use_postgeneration_results(self, step, instance, results) -> None: ...
    def get_model_class(self): ...

class _Counter:
    seq: Incomplete
    def __init__(self, seq) -> None: ...
    def next(self): ...
    def reset(self, next_value: int = ...) -> None: ...

class BaseFactory:
    UnknownStrategy: Incomplete
    UnsupportedStrategy: Incomplete
    def __new__(cls, *args, **kwargs) -> None: ...
    @classmethod
    def reset_sequence(
        cls, value: Incomplete | None = ..., force: bool = ...
    ) -> None: ...
    @classmethod
    def build(cls, **kwargs): ...
    @classmethod
    def build_batch(cls, size, **kwargs): ...
    @classmethod
    def create(cls, **kwargs): ...
    @classmethod
    def create_batch(cls, size, **kwargs): ...
    @classmethod
    def stub(cls, **kwargs): ...
    @classmethod
    def stub_batch(cls, size, **kwargs): ...
    @classmethod
    def generate(cls, strategy, **kwargs): ...
    @classmethod
    def generate_batch(cls, strategy, size, **kwargs): ...
    @classmethod
    def simple_generate(cls, create, **kwargs): ...
    @classmethod
    def simple_generate_batch(cls, create, size, **kwargs): ...

class Factory(BaseFactory, metaclass=FactoryMetaClass):
    class Meta(BaseMeta): ...

class StubObject:
    def __init__(self, **kwargs) -> None: ...

class StubFactory(Factory):
    class Meta:
        strategy: Incomplete
        model: Incomplete
    @classmethod
    def build(cls, **kwargs): ...
    @classmethod
    def create(cls, **kwargs) -> None: ...

class BaseDictFactory(Factory):
    class Meta:
        abstract: bool

class DictFactory(BaseDictFactory):
    class Meta:
        model: Incomplete

class BaseListFactory(Factory):
    class Meta:
        abstract: bool

class ListFactory(BaseListFactory):
    class Meta:
        model: Incomplete

def use_strategy(new_strategy): ...
