import os
import re
import subprocess
from functools import cached_property

import requests
from lxml import html

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class FirefoxDeveloper(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES"), "Firefox Developer Edition")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "firefox.exe"))
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://aus5.mozilla.org/update/6/Firefox/60.0/_/WINNT_x86_64-msvc-x64/en-US/aurora/_/_/_/_/update.xml"
        content = html.fromstring(requests.get(address).content)
        version = re.search("devedition-([\\db.]+)-", content.xpath("//updates/update/patch/@url")[0]).group(1)
        return version

    def download(self) -> str:
        address = "https://download.mozilla.org/?product=firefox-devedition-msi-latest-ssl&os=win64&lang=en-US"
        return from_url(address)

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            subprocess.run(f'msiexec.exe /i /qn "{package}" DESKTOP_SHORTCUT=false INSTALL_MAINTENANCE_SERVICE=false')
