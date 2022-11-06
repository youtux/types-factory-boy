from __future__ import annotations

from typing import Callable, Optional

from mypy.nodes import AssignmentStmt, NameExpr, SymbolTableNode, TypeInfo, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.types import Instance, TypeType

FACTORY_MODEL_FULLNAME = "factory.base.Factory"


def plugin(version: str) -> type[Plugin]:
    """Entry point for mypy plugin."""
    return TypesFactoryBoyPlugin


def transform_factory_model(ctx: ClassDefContext) -> None:
    """
    Configures the BaseModel subclass according to the plugin settings.
    In particular:
    * determines the model config and fields,
    * adds a fields-aware signature for the initializer and construct methods
    * freezes the class if allow_mutation = False or frozen = True
    * stores the fields, config, and if the class is settings in the mypy metadata for access by subclasses
    """
    global k
    _meta = ctx.cls.info.names.get("Meta")
    if _meta is None:
        return

    if not isinstance(_meta.node, TypeInfo):
        return

    model_symbol = _meta.node.names.get("model")
    if model_symbol is None:
        return

    if not isinstance(model_symbol.node, Var):
        return
    # for stmt in model_symbol.node.defn.defs.body:
    statements = _meta.node.defn.defs.body
    for stmt in statements:
        if isinstance(stmt, AssignmentStmt):
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
            if t is None:
                # TODO: maybe we should instead ask the ctx.api to resolve the type for this statement?
                # I'm not even sure if this is possible
                t = ctx.api.named_type(stmt.rvalue.fullname)
            if t is not None:
                break
    else:
        return

    # now let's set the type var of the class
    for base in ctx.cls.info.bases:
        if base.type.fullname == FACTORY_MODEL_FULLNAME:
            assert isinstance(t, Instance)
            # TODO: Set it only if not already set
            base.args = [t]

    return


class TypesFactoryBoyPlugin(Plugin):
    def get_base_class_hook(
        self, fullname: str
    ) -> Callable[[ClassDefContext], None] | None:
        sym = self.lookup_fully_qualified(fullname)
        if sym is None or not isinstance(sym.node, TypeInfo):  # pragma: no branch
            return None

        if any(base.fullname == FACTORY_MODEL_FULLNAME for base in sym.node.mro):
            return self._factory_model_class_maker_callback

        return None

    def _factory_model_class_maker_callback(self, ctx: ClassDefContext) -> None:
        transform_factory_model(ctx)
