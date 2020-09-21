import argparse
import asyncio
import inspect
from typing import List

from prettytable import PrettyTable

import packages
from packages import *
from services.winservice import WinService


def get_pkg_list() -> List[str]:
    """
    Return the list of available package names.

    :return: The list of available package names.
    :rtype: List[str]
    """
    return [WinService().to_cli_name(c) for c in WinService().get_cls_list(packages)]


def list() -> None:
    """..."""
    pt = PrettyTable()
    pt.field_names = ["name", "type", "info", "is_installed", "is_updated"]
    pt.align = "l"
    pt.sortby = "name"
    for pkg_name in get_pkg_list():
        pkg_inst = globals()[WinService().to_cls_name(pkg_name)]()
        pt.add_row([pkg_inst.package_name, pkg_inst.package_type, pkg_inst.package_info, "1" if pkg_inst.is_installed else "0", "1" if pkg_inst.is_updated else "0"])
    print(pt)


def install(pkg_list: List[str]) -> None:
    """
    Install all packages taking care to know if install() is asynchronous or not.

    :param pkg_list: The list of package names.
    :type pkg_list: List[str]
    """
    for pkg_name in pkg_list:
        try:
            pkg_inst = globals()[WinService().to_cls_name(pkg_name)]()
            if pkg_inst.is_updated:
                print(f"[+] The {pkg_name} package is already updated!")
            else:
                pkg_stat = "updated" if not pkg_inst.is_updated else "installed"
                if inspect.iscoroutinefunction(pkg_inst.install):
                    asyncio.run(pkg_inst.install())
                else:
                    pkg_inst.install()
                print(f"[+] The {pkg_name} package was {pkg_stat} successfully!")
        except:
            print(f"[-] The {pkg_name} package was not installed successfully!")


def main() -> None:
    parser = argparse.ArgumentParser(description="install your packages and keep them updated")
    parser.add_argument("-i", dest="packages", help="install or update the packages", metavar="p", nargs="*")
    parser.add_argument("-l", action="store_true", dest="list", help="list all packages")
    if parser.parse_args().list:
        print("[!] Generating the list of packages can take time, please be patient...")
        list()
    if parser.parse_args().packages:
        print("[!] Installing packages can take time, please be patient...")
        install(parser.parse_args().packages)


def test() -> None:
    input("[>] Press any key to continue...")


if __name__ == "__main__":
    main()
    input("[>] Press any key to continue...")
