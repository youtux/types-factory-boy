from __future__ import annotations

from mypy.plugin import Plugin


def plugin(version: str) -> type[Plugin]:
    """Entry point for mypy plugin."""
    return TypesFactoryBoyPlugin


class TypesFactoryBoyPlugin(Plugin):
    pass
