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
        return get_version(os.path.join(self.install_dir, "Figma.exe"))

    @cached_property
    def latest_version(self) -> str:
        return "9999.0.0.0"

    def download(self) -> str:
        address = "https://desktop.figma.com/win/FigmaSetup.exe"
        return from_url(address)

    def install(self) -> None:
        if self.is_updated:
            return
        program = self.download()
        subprocess.run(f'"{program}" /s /S /q /Q /quiet /silent /SILENT /VERYSILENT')
        results = []
        while not results:
            results = glob.glob(os.path.join(os.environ["USERPROFILE"], "Desktop", "Figma*.lnk"))
            time.sleep(0.5)
        os.remove(results[0])
