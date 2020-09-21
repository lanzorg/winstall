import inspect
import os
import re
from datetime import datetime
from types import ModuleType
from typing import List

import maya
import win32api


class WinService:
    def date_to_version(self, string: str) -> str:
        return maya.parse(string).datetime().strftime(r"%Y.%m.%d")

    def get_cls_list(self, cls_name: ModuleType) -> List[str]:
        return [x[0] for x in inspect.getmembers(cls_name, inspect.isclass)]

    def get_file_created(self, target: str) -> str:
        return datetime.fromtimestamp(os.path.getctime(target)).strftime(r"%Y.%m.%d")

    def get_file_modified(self, target: str) -> str:
        return datetime.fromtimestamp(os.path.getmtime(target)).strftime(r"%Y.%m.%d")

    def get_file_version(self, target: str) -> str:
        try:
            info = win32api.GetFileVersionInfo(str(target), "\\")
            ms = info["FileVersionMS"]
            ls = info["FileVersionLS"]
            return f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
        except:
            return "0"

    def to_cli_name(self, cls_name: str) -> str:
        """
        Convert class name to package name.

        :param cls_name: The class name to be converted.
        :type cls_name: str
        :return: The class name converted to package name.
        :rtype: str
        """
        return "-".join([x.casefold() for x in re.findall("[A-Z0-9][^A-Z0-9]*", cls_name)])

    def to_cls_name(self, pkg_name: str) -> str:
        """
        Convert package name to class name.

        :param pkg_name: The package name to be converted.
        :type pkg_name: str
        :return: The package name converted to class name.
        :rtype: str
        """
        return "".join([x.capitalize() for x in pkg_name.split("-")])
