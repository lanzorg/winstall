import os
import re
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class Nodejs(Package):
    """JavaScript runtime built on Chrome's V8 engine."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES"), "nodejs")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("node.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://nodejs.org/en/download/current/"
        content = requests.get(address).text
        return re.search("Current Version: <strong>([\\d.]+)</strong>", content).group(1)

    def download(self) -> str:
        address = f"https://nodejs.org/dist/v{self.last_version}/node-v{self.last_version}-x64.msi"
        return from_url(address)

    def install(self) -> None:
        if self.needs_update:
            package = self.download()
            command = f'msiexec.exe /i "{package}" /qn /norestart'
            subprocess.run(command)
