import os
import re
import subprocess

import requests

from programs.program import Program
from utilities.downloaders import from_url
from utilities.wincommons import get_file_version


class Nodejs(Program):
    @property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES"), "nodejs")

    @property
    def actual_version(self) -> str:
        return get_file_version(os.path.join(self.install_dir, "node.exe"))

    @property
    def latest_version(self) -> str:
        address = "https://nodejs.org/en/download/current/"
        content = requests.get(address).text
        version = re.search("Current Version: <strong>([\\d.]+)</strong>", content).group(1)
        return version

    def download(self) -> str:
        version = self.latest_version
        address = f"https://nodejs.org/dist/v{version}/node-v{version}-x64.msi"
        return from_url(address)

    def install(self) -> None:
        if self.is_updated:
            return
        program = self.download()
        subprocess.run(f'msiexec.exe /i "{program}" /qn /norestart')
