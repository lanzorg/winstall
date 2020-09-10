import glob
import os
import subprocess
import time
from functools import cached_property
from pathlib import Path

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version


class Figma(Package):
    """Collaborative UI design tool built in the browser."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("USERPROFILE"), "AppData", "Local", "Figma")

    @cached_property
    def package_type(self) -> str:
        return "Graphics"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("Figma.exe"))

    @cached_property
    def last_version(self) -> str:
        return "9999.9999.9999.9999"

    def download(self) -> str:
        address = "https://desktop.figma.com/win/FigmaSetup.exe"
        return from_url(address)

    def install(self) -> None:
        if self.needs_update:
            package = self.download()
            command = f'"{package}" /s /S /q /Q /quiet /silent /SILENT /VERYSILENT'
            subprocess.run(command)
            results = []
            while not results:
                results = glob.glob(Path().joinpath(os.environ["USERPROFILE"], "Desktop", "Figma*.lnk"))
                time.sleep(0.5)
            os.remove(results[0])
