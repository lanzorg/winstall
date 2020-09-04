import json
import os
import subprocess
from functools import cached_property

import requests

from programs.program import Program
from utilities.downloaders import from_url


class Yarn(Program):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES(X86)"), "Yarn")

    @cached_property
    def actual_version(self) -> str:
        return "0.0.0.0"

    @cached_property
    def latest_version(self) -> str:
        address = "https://api.github.com/repos/yarnpkg/yarn/releases/latest"
        content = requests.get(address).text
        version = json.loads(content)["name"].replace("v", "")
        return version

    def download(self) -> str:
        address = f"https://github.com/yarnpkg/yarn/releases/download/v{self.latest_version}/yarn-{self.latest_version}.msi"
        return from_url(address)

    def install(self) -> None:
        if self.is_updated:
            return
        program = self.download()
        subprocess.run(f'msiexec.exe /i "{program}" /qn /norestart')
