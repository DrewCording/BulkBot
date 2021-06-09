#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import asyncio

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('join started on bot {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    if guild.id == int(os.getenv('main_server')):
        return

    category = await guild.create_category("Bulk Orders")
    channel = await guild.create_text_channel("create-order", category=category)
    message = await channel.send("Use this to create an order form for a bulk purchase.\n\nTo create an order react with 📩")
    await message.add_reaction("📩")

    guilds_file = open("guilds_ext.list", "a")
    guilds_file.write(str(str(guild.id) + "\n"))
    guilds_file.write(str(str(category.id) + "\n"))
    guilds_file.write(str(str(channel.id) + "\n"))
    guilds_file.write(str(str(message.id) + "\n"))
    guilds_file.close()
                
client.run(os.getenv('TOKEN'))

