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
        return get_version(os.path.join(self.install_dir, "node.exe"))

    @cached_property
    def latest_version(self) -> str:
        address = "https://nodejs.org/en/download/current/"
        content = requests.get(address).text
        version = re.search("Current Version: <strong>([\\d.]+)</strong>", content).group(1)
        return version

    def download(self) -> str:
        address = f"https://nodejs.org/dist/v{self.latest_version}/node-v{self.latest_version}-x64.msi"
        return from_url(address)

    def install(self) -> None:
        if self.is_updated:
            return
        program = self.download()
        subprocess.run(f'msiexec.exe /i "{program}" /qn /norestart')