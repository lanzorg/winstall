import argparse
import asyncio
import inspect
import re
from typing import List

from prettytable import PrettyTable

import packages
from packages import *


def to_cli_name(name: str) -> str:
    """
    Convert class name to package name.

    :param name: The class name to be converted.
    :type name: str
    :return: The class name converted to package name.
    :rtype: str
    """
    return "-".join([x.casefold() for x in re.findall("[A-Z0-9][^A-Z0-9]*", name)])


def to_cls_name(name: str) -> str:
    """
    Convert package name to class name.

    :param name: The package name to be converted.
    :type name: str
    :return: The package name converted to class name.
    :rtype: str
    """
    return "".join([x.capitalize() for x in name.split("-")])


def get_pkg_list() -> List[str]:
    """
    Return the list of available package names.

    :return: The list of available package names.
    :rtype: List[str]
    """
    pkg_list = []
    cls_list = [x[0] for x in inspect.getmembers(packages, inspect.isclass)]
    for p in cls_list:
        pkg_list.append(to_cli_name(p))
    return pkg_list


def list() -> None:
    """..."""
    pt = PrettyTable()
    pt.field_names = ["package_name", "package_type", "package_info", "curr_version", "last_version", "is_installed", "needs_update"]
    pt.align = "l"
    pt.sortby = "package_name"
    for pkg_name in get_pkg_list():
        pkg_inst = globals()[to_cls_name(pkg_name)]()
        pt.add_row([pkg_inst.package_name, pkg_inst.package_type, pkg_inst.package_info, pkg_inst.curr_version, pkg_inst.last_version, pkg_inst.is_installed, pkg_inst.needs_update])
    print(pt)


def install(pkg_list: List[str]) -> None:
    """
    Install all packages taking care to know if install() is asynchronous or not.

    :param pkg_list: The list of package names.
    :type pkg_list: List[str]
    """
    for pkg_name in pkg_list:
        try:
            pkg_inst = globals()[to_cls_name(pkg_name)]()
            if not pkg_inst.needs_update:
                print(f'The "{pkg_name}" package is already updated!')
            else:
                pkg_stat = "installed" if pkg_inst.is_installed else "updated"
                if inspect.iscoroutinefunction(pkg_inst.install):
                    asyncio.run(pkg_inst.install())
                else:
                    pkg_inst.install()
                print(f'The "{pkg_name}" package was {pkg_stat} successfully!')
        except Exception as e:
            print(f'The "{pkg_name}" package was not installed successfully!')
            print(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install your packages and keep them updated.")
    parser.add_argument("-l", "--list", help="list all packages", action="store_true")
    parser.add_argument("-i", "--install", choices=get_pkg_list(), dest="packages", help="install or update the packages", metavar="package", nargs="*")
    if parser.parse_args().list:
        list()
    if parser.parse_args().packages:
        install(parser.parse_args().packages)
    input("Press any key to continue...")


def test() -> None:
    input("Press any key to continue...")


if __name__ == "__main__":
    main()
