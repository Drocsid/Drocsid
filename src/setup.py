import json
import os.path
import uuid


def generate_uuid():
    return str(uuid.uuid1())


def sanity():

    if os.path.exists("info.json"):
        with open("info.json", "r") as setup:
            unique = json.load(setup).get("uuid")
    else:
        unique = generate_uuid()
        data = {
            "uuid": f"{unique}"
        }
        with open("info.json", "w+") as setup:
            json.dump(data, setup)

    return unique
