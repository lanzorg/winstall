import os
import re
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.unarchivers import extract_dir
from utilities.wincommons import add_path, get_version


class Flutter(Package):
    """Google’s UI toolkit for building natively compiled applications."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("LOCALAPPDATA"), "Programs", "Flutter")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        try:
            content = subprocess.run(['flutter.bat', '--version'], stdout=subprocess.PIPE)
            return re.search("Flutter ([\\d.]+).*", content.stdout.decode('utf-8')).group(1)
        except:
            return "0.0.0.0"

    @cached_property
    def last_version(self) -> str:
        address = "https://storage.googleapis.com/flutter_infra/releases/releases_windows.json"
        content = requests.get(address).text
        matches = re.search("windows_([\\d.]+)([-+]?)([\\w.]*)-stable", content)
        return matches.group(1) + matches.group(2) + matches.group(3)

    def download(self) -> str:
        address = f"https://storage.googleapis.com/flutter_infra/releases/stable/windows/flutter_windows_{self.last_version}-stable.zip"
        return from_url(address)

    def install(self) -> None:
        if not self.is_installed:
            self.package_root.mkdir(exist_ok=True)
            archive = self.download()
            extract_dir(archive, self.package_root)
            add_path(self.package_root.joinpath("bin"), persisted=True)
        yep = ' '.join(["y" for _ in range(1000)])
        subprocess.run(["powershell", "flutter.bat config --no-analytics"])
        subprocess.run(["powershell", "flutter.bat upgrade"])
        subprocess.run(["powershell", f"echo {yep} | flutter.bat doctor --android-licenses"])
