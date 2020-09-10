import glob
import os
import re
import subprocess
from functools import cached_property
from pathlib import Path

import requests

from packages.package import Package
from utilities.downloaders import from_url


class Corretto(Package):
    """Multiplatform and production-ready distribution of OpenJDK from Amazon."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES"), "Amazon Corretto")

    @cached_property
    def package_type(self) -> str:
        return "Development"

    @cached_property
    def curr_version(self) -> str:
        try:
            content = subprocess.run(["java.exe", "--version"], stdout=subprocess.PIPE)
            return re.search("VM Corretto-([\\d.]+).*", content.stdout.decode("utf-8")).group(1)
        except:
            return "0.0.0.0"

    @cached_property
    def last_version(self) -> str:
        address = "https://github.com/corretto/corretto-11/releases"
        content = requests.get(address).text
        return re.search("amazon-corretto-([\\d.-]+)-windows-x64.msi", content).group(1)

    def download(self) -> str:
        address = "https://corretto.aws/downloads/latest/amazon-corretto-11-x64-windows-jdk.msi"
        return from_url(address)

    def install(self) -> None:
        if self.needs_update:
            package = self.download()
            command = f'msiexec.exe /i "{package}" INSTALLLEVEL=3 /quiet'
            subprocess.run(command)
        last_directory = max(glob.glob(str(self.package_root.joinpath("*/"))), key=os.path.getmtime)
        subprocess.run(f'setx.exe JAVA_HOME /M "{last_directory}"')
