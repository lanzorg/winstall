import json
import os
import subprocess
from functools import cached_property

import requests

from programs.program import Program
from utilities.downloaders import from_url
from utilities.wincommons import get_version, purge_desktop_links


class Chromium(Program):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES(X86)"), "Chromium")

    @cached_property
    def actual_version(self) -> str:
        return get_version(os.path.join(self.install_dir, "Application/chrome.exe")) + "-1"

    @cached_property
    def latest_version(self) -> str:
        address = "https://api.github.com/repos/tangalbert919/ungoogled-chromium-binaries/releases/latest"
        content = requests.get(address).text
        version = json.loads(content)["tag_name"]
        return version

    def download(self) -> str:
        address = f"https://github.com/tangalbert919/ungoogled-chromium-binaries/releases/download/{self.latest_version}/ungoogled-chromium_{self.latest_version}.1_installer-x64.exe"
        return from_url(address)

    def install(self) -> None:
        if self.is_updated:
            return
        program = self.download()
        if self.is_installed:
            subprocess.run(f'"{program}" --do-not-launch-chrome')
        else:
            subprocess.run(f'"{program}" --system-level --do-not-launch-chrome')
        purge_desktop_links("Chromium")
