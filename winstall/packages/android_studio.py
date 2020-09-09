import os
import re
import subprocess
import time
from functools import cached_property

import requests
from pywinauto import Desktop, keyboard

from packages.package import Package
from utilities.downloaders import from_url
from utilities.wincommons import get_version, wait_process


class AndroidStudio(Package):
    @cached_property
    def install_dir(self) -> str:
        return os.path.join(os.environ.get("PROGRAMFILES"), "Android/Android Studio")

    @cached_property
    def actual_version(self) -> str:
        version = get_version(os.path.join(self.install_dir, "bin/studio64.exe"))
        return version

    @cached_property
    def latest_version(self) -> str:
        address = "https://developer.android.com/studio/"
        content = requests.get(address).text
        version = re.search("ide-zips/([\d.]+)/android-studio-ide-([\d.]+)-windows", content).group(1)
        return version

    def download(self) -> str:
        address = "https://developer.android.com/studio/"
        content = requests.get(address).text
        matches = re.search("ide-zips/([\d.]+)/android-studio-ide-([\d.]+)-windows", content)
        address = f"https://redirector.gvt1.com/edgedl/android/studio/install/{matches.group(1)}/android-studio-ide-{matches.group(2)}-windows.exe"
        package = from_url(address)
        return package

    def install(self) -> None:
        if not self.is_updated:
            first_install = not self.is_installed
            package = self.download()
            command = f'"{package}" /S'
            subprocess.run(command)
            if first_install:
                subprocess.Popen(os.path.join(self.install_dir, "bin/studio64.exe"))
                win1 = Desktop(backend="uia").window(title_re="Import.*")
                try:
                    win1.wait("ready", timeout=10)
                    win1.set_focus()
                    keyboard.send_keys("{TAB}")
                    keyboard.send_keys("{SPACE}")
                except:
                    pass
                win2 = Desktop(backend="uia").window(title_re="Data.*")
                try:
                    win2.wait("ready", timeout=10)
                    win2.set_focus()
                    keyboard.send_keys("{SPACE}")
                except:
                    pass
                win3 = Desktop(backend="uia").window(title_re=".*Wizard")
                win3.wait("ready", timeout=100)
                win3.set_focus()
                time.sleep(5)
                keyboard.send_keys("{SPACE}")
                # Install Type
                time.sleep(5)
                keyboard.send_keys("{TAB}")
                keyboard.send_keys("{TAB}")
                keyboard.send_keys("{SPACE}")
                # Select UI Theme
                time.sleep(5)
                keyboard.send_keys("{SPACE}")
                # Verify Settings
                time.sleep(5)
                keyboard.send_keys("{TAB}")
                keyboard.send_keys("{TAB}")
                keyboard.send_keys("{TAB}")
                keyboard.send_keys("{SPACE}")
                # Downloading Components
                wait_process("studio64")
                win3.set_focus()
                keyboard.send_keys("{SPACE}")
                # Welcome  Android
                win4 = Desktop(backend="uia").window(title_re="Welcome.*Android.*")
                win4.wait("visible")
                win4.set_focus()
                win4.close()
