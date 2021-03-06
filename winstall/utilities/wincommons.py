import glob
import os
import subprocess
import time
import winreg

import psutil
from win32api import HIWORD, LOWORD, GetFileVersionInfo


def add_path(directory: str, persisted: bool = False) -> None:
    """
    Add the full path of the directory to the Windows system PATH.

    :param directory: The full path of the directory.
    :type directory: str
    :param persisted: Specify whether the PATH has to be permanently stored, defaults to False.
    :type persisted: bool, optional
    """
    if directory not in os.environ["PATH"]:
        old_path = os.environ["PATH"]        
        new_path = old_path + str(directory) if old_path.endswith(os.pathsep) else old_path + os.pathsep + str(directory)
        if persisted:
            subprocess.run('setx PATH /M "{0}"'.format(new_path))
        os.environ["PATH"] = new_path


def get_version(target: str) -> str:
    try:
        info = GetFileVersionInfo(str(target), "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        return f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}"
    except:
        return "0.0.0.0"


def purge_desktop_links(link_name: str) -> None:
    for f in glob.glob(os.path.join(os.environ["USERPROFILE"], "Desktop", f"*{link_name}*.lnk")):
        os.remove(f)
    for f in glob.glob(os.path.join("C:/Users/Public/Desktop", f"*{link_name}*.lnk")):
        os.remove(f)


def purge_keys(key0: str, key1: str, key2: str = None) -> None:
    try:
        curr_key = key1 if key2 else key1 + "\\" + key2
        open_key = winreg.OpenKey(key0, curr_key, 0, winreg.KEY_ALL_ACCESS)
        info_key = winreg.QueryInfoKey(open_key)
        for _ in range(0, info_key[0]):
            subkey = winreg.EnumKey(open_key, 0)
            try:
                winreg.DeleteKey(open_key, subkey)
            except:
                purge_keys(key0, curr_key, subkey)
        winreg.DeleteKey(open_key, "")
        open_key.Close()
    except:
        pass


def wait_process(process_name: str) -> None:
    for p in psutil.process_iter():
        if process_name.lower() in p.as_dict()["name"].lower():
            usage_list = [1.0, 1.0, 1.0, 1.0, 1.0]
            while sum(usage_list[-5:]) > 0:
                time.sleep(10)
                usage_list.append(p.cpu_percent(interval=1))
