import os
import re
import subprocess
from functools import cached_property
from pathlib import Path

import requests
from lxml import html

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class FirefoxDeveloper(Package):
    """Open-source web browser made for developers from Mozilla."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES"), "Firefox Developer Edition")

    @cached_property
    def package_type(self) -> str:
        return "Internet"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("firefox.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://aus5.mozilla.org/update/6/Firefox/60.0/_/WINNT_x86_64-msvc-x64/en-US/aurora/_/_/_/_/update.xml"
        content = html.fromstring(requests.get(address).content)
        return re.search("devedition-([\\db.]+)-", content.xpath("//updates/update/patch/@url")[0]).group(1)

    def download(self) -> str:
        address = "https://download.mozilla.org/?product=firefox-devedition-msi-latest-ssl&os=win64&lang=en-US"
        return from_url(address)

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            subprocess.run(f'msiexec.exe /i /qn "{package}" DESKTOP_SHORTCUT=false INSTALL_MAINTENANCE_SERVICE=false')
