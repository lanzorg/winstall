import glob
import os
import subprocess
import time
from functools import cached_property

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class Figma(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ["USERPROFILE"], "AppData/Local/Figma")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "Figma.exe"))
        return version

    @cached_property
    def latest_version(self) -> str:
        version = "9999.9999.9999.9999"
        return version

    def download(self) -> str:
        address = "https://desktop.figma.com/win/FigmaSetup.exe"
        package = from_url(address)
        return package

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'"{package}" /s /S /q /Q /quiet /silent /SILENT /VERYSILENT'
            subprocess.run(command)
            results = []
            while not results:
                results = glob.glob(os.path.join(os.environ["USERPROFILE"], "Desktop", "Figma*.lnk"))
                time.sleep(0.5)
            os.remove(results[0])
