import os
import re
import shutil
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from services.winservice import WinService
from utilities.downloaders import from_url
from utilities.unarchivers import extract_all
from utilities.wincommons import add_path


class AndroidSdkCmdlineTools(Package):
    """The Android SDK command line tools."""

    def __init__(self) -> None:
        self.winservice = WinService()

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("LOCALAPPDATA"), "Programs", "Android")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        return self.winservice.get_file_created(self.package_root.joinpath("cmdline-tools", "latest", "lib", "sdkmanager-classpath.jar"))

    @cached_property
    def last_version(self) -> str:
        return "0"

    def download(self) -> str:
        address = "https://developer.android.com/studio"
        content = requests.get(address).text
        release = re.search("commandlinetools-win-(\d+)_latest.zip", content).group(1)
        address = f"https://dl.google.com/android/repository/commandlinetools-win-{release}_latest.zip"
        return from_url(address)

    def install(self) -> None:
        if not self.is_installed:
            self.package_root.mkdir(exist_ok=True)
            archive = self.download()
            extract_all(archive, self.package_root)
            shutil.rmtree(self.package_root.joinpath("cmdline-tools"), ignore_errors=True)
            os.rename(self.package_root.joinpath("tools"), self.package_root.joinpath("cmdline-tools"))
            subprocess.run(f'setx.exe ANDROID_HOME /M "{self.install_dir}"')
            add_path(self.package_root.joinpath("cmdline-tools", "latest", "bin"), persisted=True)
            add_path(self.package_root.joinpath("emulator"), persisted=True)
            add_path(self.package_root.joinpath("platform-tools"), persisted=True)
        yep = " ".join(["y" for _ in range(1000)])
        subprocess.run(["powershell", f"echo {yep} | sdkmanager.bat --update"])
        subprocess.run(["powershell", f"echo {yep} | sdkmanager.bat 'platforms;android-29'"])
        subprocess.run(["powershell", f"echo {yep} | sdkmanager.bat 'build-tools;29.0.3'"])
        subprocess.run(["powershell", f"echo {yep} | sdkmanager.bat 'system-images;android-29;default;x86'"])
        subprocess.run(["powershell", f"echo {yep} | sdkmanager.bat --licenses"])
        subprocess.run(["powershell", "avdmanager create avd -k 'system-images;android-29;default;x86' -n 'pixel-xl' -d 'pixel_xl' -f"])
