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


__DISCORD_TARGETS_CHANNEL_ID = os.environ.get("DISCORD_TARGETS_CHANNEL_ID")
__DISCORD_GUILD_ID = os.environ.get("DISCORD_GUILD_ID")


async def __get_targets_channel_by_id(bot):
    guild = await bot.get_guild(__DISCORD_GUILD_ID)
    print(guild)
    return discord.utils.get(guild.channels, id=__DISCORD_TARGETS_CHANNEL_ID) 

async def __check_target_status(bot, ctx):
    message_check = 'pong!'

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
        target_channel = await __get_targets_channel_by_id(bot)
        target_message = await target_channel.fetch_message(message_id)
        json_content = json.loads(target_message.content)
        json_content['online'] = online
        await target_message.edit(content = json.dumps(json_content))


def main():
    load_dotenv() #take enviroment variables from file .env
    bot = commands.Bot(command_prefix="!")
    token = os.environ.get("DISCORD_OBSERVER_TOKEN") # should be in string type!
    api_base = "http://localhost:8000/api"

    def check_targets(sc):
        response = requests.get(f"{api_base}/targets")

        if response.text:
            targets = json.loads(response.text)

        for target in targets:
            requests.get(f"{api_base}/ping/{target['identifier']}")
        

    @bot.event
    async def on_ready():
        delay = 5
        s = sched.scheduler(time.time, time.sleep)
        s.enter(delay, 1, check_targets, (s,))
        s.run()
        

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

    bot.run(token)

if __name__ == '__main__':
    main()