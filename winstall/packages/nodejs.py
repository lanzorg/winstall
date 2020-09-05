import os
import re
import subprocess
from functools import cached_property

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class Nodejs(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES"), "nodejs")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "node.exe"))
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://nodejs.org/en/download/current/"
        content = requests.get(address).text
        version = re.search("Current Version: <strong>([\\d.]+)</strong>", content).group(1)
        return version

    def download(self) -> str:
        version = self.latest_version
        address = f"https://nodejs.org/dist/v{version}/node-v{version}-x64.msi"
        package = from_url(address)
        return package

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'msiexec.exe /i "{package}" /qn /norestart'
            subprocess.run(command)
