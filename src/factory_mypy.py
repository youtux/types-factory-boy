import re
from typing import Any

from mypy.nodes import TypeInfo, Var
from mypy.plugin import ClassDef, ClassDefContext, Plugin
from mypy.types import AnyType, Instance, TypeType

cls_found = None


def maybe_meta(ctx: ClassDefContext) -> None:
    fullname = ctx.cls.info.fullname
    # if re.search(r"\bMeta\b", fullname):
    #     print(ctx)
    #     print("Found meta:", ctx.cls)
    #     info = ctx.cls.info
    #
    #     info.names
    #
    #     1==2
    # if fullname == 'factory.base.Factory.base':
    #     print(f"Found {fullname}")
    # 1==2


def fix_class_generic_type(ctx: ClassDefContext) -> None:
    """Add a dummy __init__() to a model and record it is generated.
    Instantiation will be checked more precisely when we inferred types
    (using get_function_hook and model_hook).
    """

    cls = ctx.cls
    info = cls.info
    modified = False
    for base in info.bases:
        if base.type.fullname != "factory.base.Factory":
            continue
        if len(base.args) != 1:
            continue
        [base_arg] = base.args
        if not isinstance(base_arg, AnyType):
            if isinstance(base_arg, Instance):
                if info.fullname == "factory.base.StubFactory2":
                    global cls_found
                    cls_found = cls
                    print("Found a fixed class:", info)

            continue

        meta_attr = info.names.get("Meta", None)
        if meta_attr is None:
            continue
        meta_node = meta_attr.node
        if not isinstance(meta_node, TypeInfo):
            continue

        model_attr = meta_node.names.get("model", None)
        if model_attr is None:
            continue

        # We should just use this:
        try:
            model_cls = model_attr.type.item

        except AttributeError:
            # But it doesn't work unless the type of Meta.model is set via type annotations
            model_node = model_attr.node
            if not isinstance(model_node, Var):
                continue
            # model_cls needs to be an Instance("Foo")

            # Don't know how to fix it here...
            # model_cls = model_node.info.item
            continue

        modified = True
        base.args = (model_cls,)

    if "FooFactory" in info.fullname:
        print("FooFactory modified:", info)


class CustomPlugin(Plugin):
    # def get_type_analyze_hook(self, fullname: str):
    #     print(f"get_type_analyze_hook: {fullname}")
    def get_base_class_hook(self, fullname: str):
        # sym = self.lookup_fully_qualified(fullname)
        # print(f"get_base_class_hook: {fullname}")
        # print(sym.node.mro)
        # if sym and isinstance(sym.node, TypeInfo):
        #     if is_declarative(sym.node):
        #         return add_model_init_hook
        # return add_model_init_hook
        if fullname == "factory.base.Factory":
            return fix_class_generic_type
        return maybe_meta
        return None

    # def get_metaclass_hook(self, fullname: str):
    #     print(f"get_metaclass_hook: {fullname}")


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return CustomPlugin
