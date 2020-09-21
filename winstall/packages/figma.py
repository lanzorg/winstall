import asyncio
import glob
import os
import re
import subprocess
import time
from datetime import datetime
from functools import cached_property
from pathlib import Path

import maya
from pyppeteer import launch

from packages.package import Package
from services.webscraper import WebScraper
from services.winservice import WinService
from utilities.downloaders import from_url


class Figma(Package):
    """Collaborative UI design tool built in the browser."""

    def __init__(self) -> None:
        self.webscraper = WebScraper()
        self.winservice = WinService()

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("USERPROFILE"), "AppData", "Local", "Figma")

    @cached_property
    def package_type(self) -> str:
        return "Graphics"

    @cached_property
    def curr_version(self) -> str:
        return self.winservice.get_file_created(self.package_root.joinpath("Figma.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://releases.figma.com/"
        content = asyncio.run(self.webscraper.get_html(address))
        release = re.search('date-header"><span>(.*)<\/span>', content).group(1)
        return self.winservice.date_to_version(release)

    def download(self) -> str:
        address = "https://desktop.figma.com/win/FigmaSetup.exe"
        return from_url(address)

    def install(self) -> None:
        if not self.is_updated:
            package = self.download()
            command = f'"{package}" /s /S /q /Q /quiet /silent /SILENT /VERYSILENT'
            subprocess.run(command)
            results = []
            while not results:
                results = glob.glob(str(Path().joinpath(os.environ["USERPROFILE"], "Desktop", "Figma*.lnk")))
                time.sleep(0.5)
            os.remove(results[0])
