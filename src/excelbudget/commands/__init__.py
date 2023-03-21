import sys
from typing import Type

from .abstractcommand import AbstractCommand

# command classes
from .generate import Generate  # noqa: implicitly used by `get_cmd_cls_from_str`
from .update import Update  # noqa: implicitly used by `get_cmd_cls_from_str`
from .validate import Validate  # noqa: implicitly used by `get_cmd_cls_from_str`


def get_cmd_cls_from_str(cls_name: str) -> Type[AbstractCommand]:
    return getattr(sys.modules[__name__], cls_name)
