import json
import os
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version, purge_desktop_links


class Chromium(Package):
    """Free and open-source web browser from Google."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES(X86)"), "Chromium")

    @cached_property
    def package_type(self) -> str:
        return "Internet"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("Application", "chrome.exe")) + "-1"

    @cached_property
    def last_version(self) -> str:
        address = "https://api.github.com/repos/tangalbert919/ungoogled-chromium-binaries/releases/latest"
        content = requests.get(address).text
        return json.loads(content)["tag_name"]

    def download(self) -> str:
        address = f"https://github.com/tangalbert919/ungoogled-chromium-binaries/releases/download/{self.last_version}/ungoogled-chromium_{self.last_version}.1_installer-x64.exe"
        return from_url(address)

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'"{package}" --do-not-launch-chrome' if self.is_installed else f'"{package}" --system-level --do-not-launch-chrome'
            subprocess.run(command)
            purge_desktop_links("Chromium")
            os.system("taskkill /f /im chrome.exe")
