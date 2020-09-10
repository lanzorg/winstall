import json
import os
import re
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url


class Yarn(Package):
    """Fast, reliable, and secure dependency management."""

    @cached_property
    def package_root(self) -> Path:
        return Path().joinpath(os.environ.get("PROGRAMFILES(X86)"), "Yarn")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        try:
            content = subprocess.run(['yarn.cmd', '--version'], stdout=subprocess.PIPE)
            return re.search("([\\d.]+)", content.stdout.decode('utf-8')).group(1)
        except:
            return "0.0.0.0"

    @cached_property
    def last_version(self) -> str:
        address = "https://api.github.com/repos/yarnpkg/yarn/releases/latest"
        content = requests.get(address).text
        return json.loads(content)["name"].replace("v", "")

    def download(self) -> str:
        address = f"https://github.com/yarnpkg/yarn/releases/download/v{self.last_version}/yarn-{self.last_version}.msi"
        return from_url(address)

    def install(self) -> None:
        if self.needs_update:
            package = self.download()
            command = f'msiexec.exe /i "{package}" /qn /norestart'
            subprocess.run(command)
