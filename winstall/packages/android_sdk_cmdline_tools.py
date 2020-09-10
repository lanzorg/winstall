import os
import re
import shutil
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.unarchivers import extract_all
from utilities.wincommons import add_path


class AndroidSdkCmdlineTools(Package):
    """The Android SDK command line tools."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("LOCALAPPDATA"), "Programs", "Android")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        return "0.0.0.0"

    @cached_property
    def last_version(self) -> str:
        address = "https://developer.android.com/studio"
        content = requests.get(address).text
        return re.search("commandlinetools-win-(\d+)_latest.zip", content).group(1)

    def download(self) -> str:
        address = f"https://dl.google.com/android/repository/commandlinetools-win-{self.last_version}_latest.zip"
        return from_url(address)

    def install(self) -> None:
        if self.needs_update:
            archive = self.download()
            self.package_root.mkdir(exist_ok=True)
            extract_all(archive, self.package_root)
            shutil.rmtree(self.package_root.joinpath("cmdline-tools"), ignore_errors=True)
            os.rename(self.package_root.joinpath("tools"), self.package_root.joinpath("cmdline-tools"))
            subprocess.run(f'setx.exe ANDROID_HOME /M "{self.install_dir}"')
            add_path(self.package_root.joinpath("cmdline-tools", "bin"), persisted=True)
            add_path(self.package_root.joinpath("cmdline-tools", "emulator"), persisted=True)
            add_path(self.package_root.joinpath("cmdline-tools", "platform-tools"), persisted=True)
