import json
import os
import subprocess
from functools import cached_property

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version, purge_desktop_links


class Chromium(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES(X86)"), "Chromium")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "Application/chrome.exe")) + "-1"
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://api.github.com/repos/tangalbert919/ungoogled-chromium-binaries/releases/latest"
        content = requests.get(address).text
        version = json.loads(content)["tag_name"]
        return version

    def download(self) -> str:
        version = self.latest_version
        address = f"https://github.com/tangalbert919/ungoogled-chromium-binaries/releases/download/{version}/ungoogled-chromium_{version}.1_installer-x64.exe"
        package = from_url(address)
        return package

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'"{package}" --do-not-launch-chrome' if self.is_installed else f'"{package}" --system-level --do-not-launch-chrome'
            subprocess.run(command)
            purge_desktop_links("Chromium")
