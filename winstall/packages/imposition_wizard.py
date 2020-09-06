import glob
import os
import re
import shutil
import subprocess
from functools import cached_property

import requests

from packages.package import Package
from utilities.downloaders import from_filecr
from utilities.unarchivers import extract_dir
from utilities.wincommons import get_version, purge_desktop_links


class ImpositionWizard(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES"), "Appsforlife/Imposition Wizard 3")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "ImpositionWizard.exe"))
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://filecr.com/windows/imposition-wizard/"
        content = requests.get(address).text
        version = re.search("<h2>Imposition Wizard (.*)</h2>", content).group(1)
        return version

    async def download(self) -> str:
        archive = await from_filecr("https://filecr.com/windows/imposition-wizard/")
        return archive

    async def install(self) -> None:
        if not self.is_updated:
            archive = await self.download()
            destination = extract_dir(archive, password="123")
            package = glob.glob(f"{destination}/*.exe")[0]
            command = f'"{package}" /S'
            subprocess.run(command)
            source = os.path.join(destination, "crack/ImpositionWizard.exe")
            target = os.path.join(self.install_dir, "ImpositionWizard.exe")
            shutil.copy(source, target)
            purge_desktop_links("Imposition Wizard")
