import os
import re
import json
import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
from idna import check_nfc
from features.setup import check_target_status, generate_uuid
import requests

__DISCORD_TARGETS_CHANNEL_NAME = "targets"
__DISCORD_TARGETS_CHANNEL_ID = os.environ.get("DISCORD_TARGETS_CHANNEL_ID")

def main():
    load_dotenv() #take enviroment variables from file .env
    bot = commands.Bot(command_prefix="!")
    token = os.environ.get("DISCORD_OBSERVER_TOKEN") # should be in string type!
    api_base = "http://localhost:8000/api"

    def check_targets():
        delay = 30
        threading.Timer(delay, check_targets).start()
        response = requests.get(f"{api_base}/targets")

        if response.text:
            targets = json.loads(response.text)

        for target in targets:
            requests.get(f"{api_base}/ping/{target['identifier']}")

    @bot.event
    async def on_ready():
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
        targets_channel = discord.utils.get(guild.text_channels, name=__DISCORD_TARGETS_CHANNEL_NAME)

        await targets_channel.send(json.dumps({
            'identifier': channel.name,
            'channel_id': channel.id,
            'metadata': channel.topic,
            'online': True
        }))
        
    @bot.command()
    async def ping(ctx):
        await check_target_status(bot, ctx)

    bot.run(token)

if __name__ == '__main__':
    main()