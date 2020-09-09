import os
import pathlib
import re
import shutil
import subprocess
from functools import cached_property

import requests

from packages.package import Package
from utilities.downloaders import from_url
from utilities.unarchivers import extract_all
from utilities.wincommons import add_path


class AndroidSdk(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("LOCALAPPDATA"), "Programs", "Android")

    @cached_property
    def actual_version(self) -> str:
        version = "0.0.0.0"
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://developer.android.com/studio"
        content = requests.get(address).text
        version = re.search("commandlinetools-win-(\d+)_latest.zip", content).group(1)
        return version

    def download(self) -> str:
        version = self.latest_version
        address = f"https://dl.google.com/android/repository/commandlinetools-win-{version}_latest.zip"
        archive = from_url(address)
        return archive

    def install(self) -> None:
        if not self.is_updated:
            archive = self.download()
            pathlib.Path(self.install_dir).mkdir(exist_ok=True)
            extract_all(archive, self.install_dir)
            shutil.rmtree(pathlib.Path(self.install_dir).joinpath("cmdline-tools"), ignore_errors=True)
            os.rename(os.path.join(self.install_dir, "tools"), os.path.join(self.install_dir, "cmdline-tools"))
            subprocess.run(f'setx.exe ANDROID_HOME /M "{self.install_dir}"')
            add_path(os.path.join(self.install_dir, "cmdline-tools", "bin"), persisted=True)
            add_path(os.path.join(self.install_dir, "cmdline-tools", "emulator"), persisted=True)
            add_path(os.path.join(self.install_dir, "cmdline-tools", "platform-tools"), persisted=True)
