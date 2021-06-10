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
    print('message sync started on bot {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.channel.category_id == int(os.getenv('ext_order_cat')):
        order_ext_file = open("order_ext.list", "r")
        order_ext_list = order_ext_file.readlines()
        order_ext_file.close()
        order_ext_list = list(map(str.strip, order_ext_list))

        if str(message.channel.id) in order_ext_list:
            index = int(order_ext_list.index(str(message.channel.id)))
            ext_guild = client.get_guild(int(order_ext_list[int(index-3)]))
            ext_channel = ext_guild.get_channel(int(order_ext_list[int(index-2)]))

            await ext_channel.send("[" + str(message.author) + "] " + message.content)

    else:
        order_ext_file = open("order_ext.list", "r")
        order_ext_list = order_ext_file.readlines()
        order_ext_file.close()
        order_ext_list = list(map(str.strip, order_ext_list))

        if str(message.channel.id) in order_ext_list:
            index = int(order_ext_list.index(str(message.channel.id)))
            main_guild = client.get_guild(int(os.getenv('main_server')))
            main_channel = main_guild.get_channel(int(order_ext_list[int(index+2)]))

            await main_channel.send("[" + str(message.author) + "] " + message.content)

client.run(os.getenv('TOKEN'))

