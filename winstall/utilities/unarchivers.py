import os
import re
import shutil
import subprocess
from tempfile import mkdtemp

import requests

from utilities.downloaders import from_url
from utilities.wincommons import add_path


def _initialize() -> str:
    """
    Download 7z.exe and add it to the Windows PATH if not already present.

    :return: The "7z.exe" string.
    :rtype: str
    """
    if not shutil.which("7z.exe"):
        content = requests.get("https://www.7-zip.org/download.html").text
        pattern = "Download 7-Zip ([\d.]+)"
        version = re.findall(pattern, content)[0].replace(".", "")
        package = from_url("https://7-zip.org/a/7z{0}-x64.msi".format(version))
        for r, d, f in os.walk(extract_msi(package)):
            for name in f:
                if name == "7z.exe":
                    add_path(r)
    return "7z.exe"


def extract_all(archive: str, destination: str = None, password: str = None) -> str:
    """
    Extract the whole files from the archive.

    :param archive: The full path of the archive.
    :type archive: str
    :param destination: The full path of the extraction directory, defaults to None.
    :type destination: str, optional
    :param password: The password for the archive, defaults to None.
    :type password: str, optional
    :return: The full path of the extraction directory.
    :rtype: str
    """
    if not destination:
        destination = mkdtemp()
    if password:
        subprocess.run('{0} x "{1}" -o"{2}" -p"{3}" -y -bso0 -bsp0'.format(_initialize(), archive, destination, password))
    else:
        subprocess.run('{0} x "{1}" -o"{2}" -y -bso0 -bsp0'.format(_initialize(), archive, destination))
    return destination


def extract_dir(archive: str, destination: str = None, password: str = None) -> str:
    """
    Extract the whole files from the first directory of the archive.

    :param archive: The full path of the archive.
    :type archive: str
    :param destination: The full path of the extraction directory, defaults to None.
    :type destination: str, optional
    :param password: The password for the archive, defaults to None.
    :type password: str, optional
    :return: The full path of the extraction directory.
    :rtype: str
    """
    if not destination:
        destination = mkdtemp()
    shutil.copytree(next(os.scandir(extract_all(archive, mkdtemp(), password))).path, destination, dirs_exist_ok=True)
    return destination


def extract_msi(package: str, destination: str = None) -> str:
    """
    Extract the whole files from the .msi package.

    :param package: The full path of the .msi package.
    :type package: str
    :param destination: The full path of the extraction directory, defaults to None.
    :type destination: str, optional
    :return: The full path of the extraction directory.
    :rtype: str
    """
    if not destination:
        destination = mkdtemp()
    subprocess.run("msiexec.exe /a {0} /q TARGETDIR={1}".format(package, destination))
    return destination
