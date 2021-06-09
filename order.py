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
    print('order started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    if payload.guild_id == int(os.getenv('main_server')):
        if payload.channel_id == int(os.getenv('order_chan')):
            if payload.message_id == int(os.getenv('order_msg')):
                channel = client.get_channel(payload.channel_id)
                await asyncio.sleep(0.3)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)
                if str(payload.emoji.name) == "📩":
                    user = message.guild.get_member(payload.user_id)
                    category = client.get_channel(int(os.getenv('int_order_cat')))

                    index_file = open("order.index", "r")
                    index = index_file.readlines()
                    index_file.close()

                    index = len(index) + 1
                       
                    index_file = open("order.index", "a")
                    index_file.write(str(str(index) + "\n"))
                    index_file.close()

                    order_chan = await message.guild.create_text_channel(str("Order-" + str(index)), category=category)
                    await order_chan.set_permissions(user, read_messages=True, send_messages=True)

                    order_file = open("order.msg", "r")
                    order_message = await order_chan.send("Hey <@!" + str(user.id) + ">, you have created a new order.\n\n" + str(order_file.read()))
                    order_file.close()

                    order_file = open("order_int.list", "a")
                    order_file.write(str(str(order_message.id) + "\n"))
                    order_file.close()

                    await order_message.add_reaction("🔒")
                    await order_message.pin()

    else:
        guilds_file = open("guilds_ext.list", "r")
        guilds_list = guilds_file.readlines()
        guilds_file.close()
        guilds_list = list(map(str.strip, guilds_list))

        if str(payload.guild_id) in guilds_list:
            if str(payload.channel_id) in guilds_list:
                if str(payload.message_id) in guilds_list:
                    channel = client.get_channel(payload.channel_id)
                    await asyncio.sleep(0.3)
                    message = await channel.fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, payload.member)
                    if str(payload.emoji.name) == "📩":
                        user = message.guild.get_member(payload.user_id)
                        category = client.get_channel(channel.category_id)
                        main_category = client.get_channel(int(os.getenv('ext_order_cat')))
                        main_guild = client.get_guild(int(os.getenv('main_server')))

                        index_file = open("order.index", "r")
                        index = index_file.readlines()
                        index_file.close()

                        index = len(index) + 1
                       
                        index_file = open("order.index", "a")
                        index_file.write(str(str(index) + "\n"))
                        index_file.close()

                        order_chan = await message.guild.create_text_channel(str("Order-" + str(index)), category=category)
                        await order_chan.set_permissions(message.guild.default_role, read_messages=False, send_messages=False)
                        await order_chan.set_permissions(user, read_messages=True, send_messages=True)

                        main_order_chan = await main_guild.create_text_channel(str("Order-" + str(index)), category=main_category)
                        
                        order_file = open("order.msg", "r")
                        order_message = await order_chan.send("Hey <@!" + str(user.id) + ">, you have created a new order.\n\n" + str(order_file.read()))
                        order_file.close()

                        main_order_message = await main_order_chan.send(str(user) + " has created a new order on their server, " + str(message.guild.name) + "\n\nTo close this order react with :lock:")

                        order_file = open("order_ext.list", "a")
                        order_file.write(str(str(message.guild.id) + "\n"))
                        order_file.write(str(str(order_chan.id) + "\n"))
                        order_file.write(str(str(order_message.id) + "\n"))
                        order_file.write(str(str(main_order_chan.id) + "\n"))
                        order_file.write(str(str(main_order_message.id) + "\n"))
                        order_file.close()

                        await order_message.add_reaction("🔒")
                        await order_message.pin()

                        await main_order_message.add_reaction("🔒")
                        await order_message.pin()
                
client.run(os.getenv('TOKEN'))

