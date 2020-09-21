import glob
import os
import re
import shutil
import subprocess
import time
import winreg
from functools import cached_property
from pathlib import Path

import requests
from pywinauto import Desktop, keyboard

from packages.package import Package
from utilities.downloaders import from_filecr
from utilities.unarchivers import extract_dir
from utilities.wincommons import get_version, purge_keys


class Antidote(Package):
    """Grammar corrector with rich dictionaries and language guides."""

    @cached_property
    def package_root(self) -> str:
        return Path().joinpath(os.environ.get("PROGRAMFILES(X86)"), "Druide")

    @cached_property
    def package_type(self) -> str:
        return "Office"

    @cached_property
    def curr_version(self) -> str:
        return get_version(self.package_root.joinpath("Antidote 10", "Application", "Bin64", "Antidote.exe"))

    @cached_property
    def last_version(self) -> str:
        address = "https://filecr.com/windows/antidote/"
        content = requests.get(address).text
        return re.search("<h2>Antidote (.*)</h2>", content).group(1).replace(" ", ".").replace("v", "")

    async def download(self) -> str:
        return await from_filecr("https://filecr.com/windows/antidote/")

    async def install(self) -> None:
        if not self.is_installed:
            self._remove_leftovers()
            archive = await self.download()
            destination = extract_dir(archive, password="123")
            setup_dir = Path().joinpath(destination, "Setup - retail", "msi", "druide")
            subprocess.run(f'msiexec.exe /qn /i "{setup_dir}\\Antidote10.msi" TRANSFORMS="{setup_dir}\\Antidote10-Interface-en.mst"')
            subprocess.run(f'msiexec.exe /qn /i "{setup_dir}\\Antidote10-Module-francais.msi" TRANSFORMS="{setup_dir}\\Antidote10-Module-francais-Interface-en.mst"')
            subprocess.run(f'msiexec.exe /qn /i "{setup_dir}\\Antidote10-English-module.msi" TRANSFORMS="{setup_dir}\\Antidote10-English-module-Interface-en.mst"')
            subprocess.run(f'msiexec.exe /qn /i "{setup_dir}\\Antidote-Connectix10.msi" TRANSFORMS="{setup_dir}\\Antidote-Connectix10-Interface-en.mst"')
            updates_dir = os.path.join(destination, "Updates")
            for msp_file in glob.glob(os.path.join(updates_dir, "*.msp")):
                subprocess.run(f'msiexec.exe /qn /p "{msp_file}"')
            shutil.copy(Path().joinpath(destination, "Crack", "Antidote.exe"), self.package_root.joinpath("Antidote 10", "Application", "Bin64", "Antidote.exe"))
            os.system("taskkill /f /im chrome.exe")
            self._post_install()
        
    def _hide_connectix_icon(self) -> None:
        subprocess.Popen(self.package_root.joinpath("Connectix 10", "Application", "Bin64", "Connectix.exe"))
        win1 = Desktop(backend="uia").window(title="Connectix")
        win1.wait("visible", timeout=20)
        win1.set_focus()
        keyboard.send_keys("^R")
        win2 = Desktop(backend="uia").window(title_re="Options.*")
        win2.wait("visible")
        win2.set_focus()
        keyboard.send_keys("{TAB 4}")
        keyboard.send_keys("{SPACE}")
        keyboard.send_keys("{TAB 10}")
        keyboard.send_keys("{SPACE}")
        win1.close()

    def _post_install(self) -> None:
        subprocess.Popen(self.package_root.joinpath("Antidote 10", "Application", "Bin64", "Antidote.exe"))
        # Handle the 1st window.
        win1 = Desktop(backend="uia").window(class_name="Qt5QWindowIcon")
        win1.wait("visible", timeout=20)
        win1.set_focus()
        link = win1["Enter a serial number…"]
        link.click_input()
        # Handle the 2nd window.
        time.sleep(3)
        win2 = Desktop(backend="uia").window(class_name="Qt5QWindowIcon")
        win2.wait("visible")
        win2.set_focus()
        keyboard.send_keys("John")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("Doe")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("123-456-789-012")
        keyboard.send_keys("{SPACE}")
        # Handle the 3rd window.
        time.sleep(3)
        win3 = Desktop(backend="uia").window(class_name="Qt5QWindowIcon")
        win3.wait("visible")
        win3.set_focus()
        keyboard.send_keys("FV-12345-67890-1234-67890-123455")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        # Handle the 4th window.
        time.sleep(3)
        win4 = Desktop(backend="uia").Antidote
        win4.wait("visible")
        win4.set_focus()
        keyboard.send_keys("{SPACE}")
        # Handle the 5th window.
        time.sleep(3)
        win5 = Desktop(backend="uia").window(title_re="Personalize.*")
        win5.wait("visible")
        win5.set_focus()
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        # Handle the 6th window.
        time.sleep(3)
        win6 = Desktop(backend="uia").window(title_re="Personalize.*")
        win6.wait("visible")
        win6.set_focus()
        keyboard.send_keys("{SPACE}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{ENTER}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        keyboard.send_keys("{TAB}")
        keyboard.send_keys("{SPACE}")
        # Kill all related processes.
        time.sleep(3)
        os.system("taskkill /f /im Antidote.exe")
        os.system("taskkill /f /im Connectix.exe")
        os.system("taskkill /f /im AgentAntidote.exe")
        os.system("taskkill /f /im AgentConnectix.exe")
        time.sleep(3)
        # Hide the connectix icon from taskbar.
        self._hide_connectix_icon()

    def _remove_leftovers(self) -> None:
        if os.path.exists("C:/Windows/AM213468.bin"):
            os.remove("C:/Windows/AM213468.bin")
        if os.path.exists("C:/Windows/system32/WS022057.bin"):
            os.remove("C:/Windows/system32/WS022057.bin")
        purge_keys(winreg.HKEY_CURRENT_USER, "Software\Druide informatique inc.")
        purge_keys(winreg.HKEY_LOCAL_MACHINE, "Software\Druide informatique inc.")
        shutil.rmtree(Path().joinpath(os.environ["USERPROFILE"], "AppData", "Roaming", "Druide"), ignore_errors=True)
        shutil.rmtree(self.package_root, ignore_errors=True)
