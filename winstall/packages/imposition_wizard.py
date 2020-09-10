import glob
import os
import re
import shutil
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_filecr
from utilities.unarchivers import extract_dir
from utilities.wincommons import get_version, purge_desktop_links


class ImpositionWizard(Package):
    """PDF imposition software with simple user interface and realtime preview."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES"), "Appsforlife", "Imposition Wizard 3")

    @cached_property
    def package_type(self) -> str:
        return "Office"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("ImpositionWizard.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://filecr.com/windows/imposition-wizard/"
        content = requests.get(address).text
        return re.search("<h2>Imposition Wizard (.*)</h2>", content).group(1)

    async def download(self) -> str:
        return await from_filecr("https://filecr.com/windows/imposition-wizard/")

    async def install(self) -> None:
        if self.needs_update:
            archive = await self.download()
            destination = extract_dir(archive, password="123")
            package = glob.glob(f"{destination}/*.exe")[0]
            command = f'"{package}" /S'
            subprocess.run(command)
            source = Path(destination).joinpath("crack", "ImpositionWizard.exe")
            target = self.package_root.joinpath("ImpositionWizard.exe")
            shutil.copy(source, target)
            purge_desktop_links("Imposition Wizard")
