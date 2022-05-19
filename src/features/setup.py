import json
import os
import uuid
import discord
from dotenv import load_dotenv
import os as osVars
from discord.ext import commands

# generate uuid using the target's mac address
def generate_uuid():
    return str(uuid.getnode())