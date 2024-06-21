from __future__ import annotations

import functools
import logging
from typing import Callable

from mypy.errorcodes import ATTR_DEFINED
from mypy.messages import format_type
from mypy.nodes import AssignmentStmt, NameExpr, TypeInfo, Var
from mypy.plugin import AttributeContext, ClassDefContext, Plugin
from mypy.subtypes import find_member
from mypy.types import AnyType, Instance, Type, TypeType

FACTORY_MODEL_FULLNAME = "factory.base.Factory"

logger = logging.getLogger(__name__)

# TODO: Figure out how to invoke mypy so that we get these logs, and then remove this
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def plugin(version: str) -> type[Plugin]:
    """Entry point for mypy plugin."""
    return TypesFactoryBoyPlugin


def transform_factory_model(ctx: ClassDefContext) -> None:
    """
    Configures the Factory subclass.
    """
    _meta = ctx.cls.info.names.get("Meta")
    if _meta is None:
        return

    if not isinstance(_meta.node, TypeInfo):
        return

    bases_to_replace = [
        base
        for base in ctx.cls.info.bases
        if base.type.fullname == FACTORY_MODEL_FULLNAME
        and isinstance(base.args[0], AnyType)
    ]

    if bases_to_replace:
        for base in bases_to_replace:
            logger.info(
                "Found base class %s for %s with AnyType. Proceeding.",
                base,
                ctx.cls.fullname,
            )
    if not bases_to_replace:
        logger.info(
            "All bases for %s already parametrized. Skipping.", ctx.cls.fullname
        )
        return

    model_symbol = _meta.node.names.get("model")
    if model_symbol is None:
        return

    if not isinstance(model_symbol.node, Var):
        return
    # for stmt in model_symbol.node.defn.defs.body:
    statements = _meta.node.defn.defs.body
    for stmt in statements:
        if not isinstance(stmt, AssignmentStmt):
            continue

        lvalue = stmt.lvalues[0]
        if not isinstance(lvalue, NameExpr):
            continue
        if lvalue.name != "model":
            continue
        t = None
        if stmt.type is not None:
            if not isinstance(stmt.type, TypeType):
                # TODO: log an error
                pass
            else:
                t = stmt.type.item
                assert isinstance(t, Instance)
        if t is None:
            # TODO: maybe we should instead ask the ctx.api to resolve the type for this statement?
            # I'm not even sure if this is possible
            t = ctx.api.named_type(stmt.rvalue.fullname)
        if t is not None:
            break
    else:
        return

    # now let's set the type var of the class
    for base in bases_to_replace:
        logger.info(
            "Replacing type var for base %s of %s with %s", base, ctx.cls.fullname, t
        )
        base.args = [t]

    return


def _resolver_attribute(ctx: AttributeContext, *, attr: str) -> Type:
    # We use 'Any' as the '__getattr__' return value
    # allow existing attributes to be returned as normal if they are not of type Any.
    # We can just check against Any because it's not used on any other attribute of the class.
    # If it was the case, we should improve the check.
    # TODO: Improve the check so that we can have Any return type on other attributes of the class.
    if not isinstance(ctx.default_attr_type, AnyType):
        # We use Any only in the declaration of __missing__ in the Resolver class
        # so we will use Any as a singleton to check against
        return ctx.default_attr_type
    assert isinstance(ctx.type, Instance), ctx.type
    assert len(ctx.type.args) == 1, ctx.type
    assert isinstance(ctx.type.args[0], Instance), ctx.type
    generic_type = ctx.type.args[0]
    member = find_member(attr, generic_type, generic_type)
    if member is None:
        ctx.api.fail(
            f"{format_type(ctx.type, ctx.api.options)} has no attribute {attr}",
            ctx.context,
            code=ATTR_DEFINED,
        )
        return ctx.default_attr_type
    else:
        return member


class TypesFactoryBoyPlugin(Plugin):
    def get_attribute_hook(
        self,
        fullname: str,
    ) -> Callable[[AttributeContext], Type] | None:
        # fullname: lazy.Lazy.foo
        if fullname.startswith("factory.builder.Resolver."):
            _, _, attr = fullname.rpartition(".")
            return functools.partial(_resolver_attribute, attr=attr)
        return None

    # def get_base_class_hook(
    #     self, fullname: str
    # ) -> Callable[[ClassDefContext], None] | None:
    #     sym = self.lookup_fully_qualified(fullname)
    #     if sym is None or not isinstance(sym.node, TypeInfo):  # pragma: no branch
    #         return None
    #
    #     if any(base.fullname == FACTORY_MODEL_FULLNAME for base in sym.node.mro):
    #         return self._factory_model_class_maker_callback
    #
    #     return None
    #
    # def _factory_model_class_maker_callback(self, ctx: ClassDefContext) -> None:
    #     transform_factory_model(ctx)
