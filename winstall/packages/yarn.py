import json
import os
import subprocess
from functools import cached_property

import requests

from packages.package import Package
from utilities.downloaders import from_url


class Yarn(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES(X86)"), "Yarn")

    @cached_property
    def actual_version(self) -> str:
        version = "0.0.0.0"
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://api.github.com/repos/yarnpkg/yarn/releases/latest"
        content = requests.get(address).text
        version = json.loads(content)["name"].replace("v", "")
        return version

    def download(self) -> str:
        version = self.latest_version
        address = f"https://github.com/yarnpkg/yarn/releases/download/v{version}/yarn-{version}.msi"
        package = from_url(address)
        return package

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'msiexec.exe /i "{package}" /qn /norestart'
            subprocess.run(command)
