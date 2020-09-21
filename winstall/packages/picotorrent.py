import json
import os
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class Picotorrent(Package):
    """Tiny and hackable BitTorrent client."""

    @cached_property
    def package_root(self) -> Path:
        return Path().joinpath(os.environ.get("PROGRAMFILES"), "PicoTorrent")

    @cached_property
    def package_type(self) -> str:
        return "Internet"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("PicoTorrent.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://api.github.com/repos/picotorrent/picotorrent/releases/latest"
        content = requests.get(address).text
        return json.loads(content)["tag_name"].replace("v", "")

    def download(self) -> None:
        address = f"https://github.com/picotorrent/picotorrent/releases/download/v{self.last_version}/PicoTorrent-{self.last_version}-x64.exe"
        return from_url(address)

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'"{package}" /passive /quiet /norestart'
            subprocess.run(command)
