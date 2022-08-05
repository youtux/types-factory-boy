from dataclasses import dataclass
from typing import Type

import factory


@dataclass
class Foo:
    ...


class FooFactory(factory.Factory):
    class Meta:
        model: Type[Foo] = Foo


reveal_type(FooFactory.Meta.model)

foo = FooFactory.create()

reveal_type(foo)

assert isinstance(foo, Foo)
