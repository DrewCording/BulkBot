#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import asyncio
import mysql.connector
from datetime import datetime

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('db_password'),
    database="burnt_bot"
)

@client.event
async def on_ready():
    print('order close started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    channel = client.get_channel(payload.channel_id)
    channel_cat = channel.category

    if payload.guild_id == int(os.getenv('main_server')):
        if channel_cat.id == int(os.getenv('int_order_cat')):
            order_int_file = open("order_int.list", "r")
            order_int_list = order_int_file.readlines()
            order_int_file.close()
            order_int_list = list(map(str.strip, order_int_list))

            if str(payload.message_id) in order_int_list:
                await asyncio.sleep(0.3)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)

                if str(payload.emoji.name) == "🔒":
                    order_int_list.remove(str(payload.message_id))

                    order_int_file = open("order_int.list", "w")
                    for order in order_int_list:
                        order_int_file.write(str(order + "\n"))
                    order_int_file.close()

                    await channel.send("This order has been closed by <@!" + str(payload.user_id) + ">")
                    await channel.edit(name=str("Closed-" + str(channel.name)))

                    msg_ptrn = "<@!(.*?)>"
                    user_id = re.search(msg_ptrn, message.content)
                    buyer = message.guild.get_member(int(user_id.group(1)))
                    await channel.set_permissions(buyer, read_messages=True, send_messages=False)
                    
                    closer = message.guild.get_member(int(payload.user_id))
                    mod_role = discord.utils.get(message.guild.roles, name=os.getenv('mod_role'))
                    value_chan = await message.guild.create_text_channel(str(str(channel.name).replace("closed", "commission")))
                    await value_chan.set_permissions(message.guild.default_role, read_messages=False, send_messages=False)
                    await value_chan.set_permissions(closer, read_messages=True, send_messages=True)
                    await value_chan.set_permissions(mod_role, read_messages=True, send_messages=True)
                    await value_chan.send("Hey <@!" + str(closer.id) + ">, you just closed an order. Please tell me the total profit of that order so I can correctly calculate the commission.\nSimply respond '500' or '10365K' or '500M' or '2B' for example.\nThis value should be in OSRS gp.\n\nYou have 24 hours to provide the value or this order will be flagged for mod review.")
                    
                    def check(m):
                        return m.channel == value_chan

                    invalid=1

                    while invalid:
                        msg = await client.wait_for('message', check=check)

                        if str(msg.content).isnumeric():
                            num = int(msg.content)
                            mult = 1
                            invalid=0
                        else:
                            if str(msg.content[:-1]).isnumeric():
                                num = int(msg.content[:-1])
                                mult = str(msg.content[-1]).lower()

                                if mult in ['k', 'm', 'b']:
                                    invalid=0

                        if invalid: 
                            await value_chan.send("That input was not valid, please try again.\nYour input should only be a number and a letter (k, m, or b) and nothing else.")

                    await value_chan.send("Thank you, your input has been recorded.\nThis channel will self destruct in 24 hours.")

                    if mult == 'k':
                        mult = int(1000)
                    elif mult == 'm':
                        mult = int(1000000)
                    elif mult == 'b':
                        mult = int(1000000000)

                    value = num * mult
                    commission = int(value * float(os.getenv('commission')))
                    dev_fee = int(value * float(os.getenv('dev_fee')))

                    mycursor = mydb.cursor()
                    mycursor.execute(str("SELECT * FROM buyers WHERE id=" + str(buyer.id)))
                    commissioner = mycursor.fetchall()

                    if commissioner:
                        sql = "INSERT INTO commissions (date, name, id, buyer, amount) VALUES (%s, %s, %s, %s, %s)"
                        val = (str(datetime.now()), str(commissioner[0][3]), str(commissioner[0][4]), str(buyer), str(commission))
                        mycursor.execute(sql, val)
                        mydb.commit()
                    
                    developer = message.guild.get_member(int(os.getenv('developer')))
                    sql = "INSERT INTO commissions (date, name, id, buyer, amount) VALUES (%s, %s, %s, %s, %s)"
                    val = (str(datetime.now()), str(developer), str(developer.id), str(buyer), str(dev_fee))
                    mycursor.execute(sql, val)
                    mydb.commit()

                    await asyncio.sleep(1440)
                    await value_chan.delete()

        elif channel_cat.id == int(os.getenv('ext_order_cat')):
            order_ext_file = open("order_ext.list", "r")
            order_ext_list = order_ext_file.readlines()
            order_ext_file.close()
            order_ext_list = list(map(str.strip, order_ext_list))

            if str(payload.message_id) in order_ext_list:
                await asyncio.sleep(0.3)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)

                if str(payload.emoji.name) == "🔒":
                    index = int(order_ext_list.index(str(message.id)))
                    ext_guild = client.get_guild(int(order_ext_list[int(index-4)]))
                    ext_channel = ext_guild.get_channel(int(order_ext_list[int(index-3)]))
                    ext_message = await ext_channel.fetch_message(int(order_ext_list[int(index-2)]))
                    user = client.get_user(payload.user_id)

                    await channel.send("This order has been closed by <@!" + str(payload.user_id) + ">\nIt will no longer sync between servers")
                    await channel.edit(name=str("Closed-" + str(channel.name)))

                    await ext_channel.send("This order has been closed by " + str(user) + "\nIt will no longer sync between servers")
                    await ext_channel.edit(name=str("Closed-" + str(ext_channel.name)))

                    del order_ext_list[int(index-4):int(index+1)]

                    order_ext_file = open("order_ext.list", "w")
                    for order in order_ext_list: 
                        order_ext_file.write(str(order + "\n"))
                    order_ext_file.close()

                    msg_ptrn = "<@!(.*?)>"
                    user_id = re.search(msg_ptrn, ext_message.content)
                    buyer = ext_message.guild.get_member(int(user_id.group(1)))
                    await ext_channel.set_permissions(buyer, read_messages=True, send_messages=False)

                    closer = message.guild.get_member(int(payload.user_id))
                    mod_role = discord.utils.get(message.guild.roles, name=os.getenv('mod_role'))
                    value_chan = await message.guild.create_text_channel(str(str(channel.name).replace("closed", "commission")))
                    await value_chan.set_permissions(message.guild.default_role, read_messages=False, send_messages=False)
                    await value_chan.set_permissions(closer, read_messages=True, send_messages=True)
                    await value_chan.set_permissions(mod_role, read_messages=True, send_messages=True)
                    await value_chan.send("Hey <@!" + str(closer.id) + ">, you just closed an order. Please tell me the total profit of that order so I can correctly calculate the commission.\nSimply respond '500' or '10365K' or '500M' or '2B' for example.\nThis value should be in OSRS gp.\n\nYou have 24 hours to provide the value or this order will be flagged for mod review.")
                    
                    def check(m):
                        return m.channel == value_chan

                    invalid=1

                    while invalid:
                        msg = await client.wait_for('message', check=check)

                        if str(msg.content).isnumeric():
                            num = int(msg.content)
                            mult = 1
                            invalid=0
                        else:
                            if str(msg.content[:-1]).isnumeric():
                                num = int(msg.content[:-1])
                                mult = str(msg.content[-1]).lower()

                                if mult in ['k', 'm', 'b']:
                                    invalid=0

                        if invalid: 
                            await value_chan.send("That input was not valid, please try again.\nYour input should only be a number and a letter (k, m, or b) and nothing else.")

                    await value_chan.send("Thank you, your input has been recorded.\nThis channel will self destruct in 24 hours.")

                    if mult == 'k':
                        mult = int(1000)
                    elif mult == 'm':
                        mult = int(1000000)
                    elif mult == 'b':
                        mult = int(1000000000)

                    value = num * mult
                    dev_fee = int(value * float(os.getenv('dev_fee')))

                    mycursor = mydb.cursor()
                    developer = message.guild.get_member(int(os.getenv('developer')))
                    sql = "INSERT INTO commissions (date, name, id, buyer, amount) VALUES (%s, %s, %s, %s, %s)"
                    val = (str(datetime.now()), str(developer), str(developer.id), str(buyer), str(dev_fee))
                    mycursor.execute(sql, val)
                    mydb.commit()

                    await asyncio.sleep(1440)
                    await value_chan.delete()
                    

    else:
        order_ext_file = open("order_ext.list", "r")
        order_ext_list = order_ext_file.readlines()
        order_ext_file.close()
        order_ext_list = list(map(str.strip, order_ext_list))

        if str(payload.message_id) in order_ext_list:
            await asyncio.sleep(0.3)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)

            if str(payload.emoji.name) == "🔒":
                index = int(order_ext_list.index(str(message.id)))
                main_guild = client.get_guild(int(os.getenv('main_server')))
                main_channel = main_guild.get_channel(int(order_ext_list[int(index+1)]))
                user = client.get_user(payload.user_id)

                await channel.send("This order has been closed by <@!" + str(payload.user_id) + ">\nIt will no longer sync between servers")
                await channel.edit(name=str("Closed-" + str(channel.name)))

                await main_channel.send("This order has been closed by " + str(user) + "\nIt will no longer sync between servers")
                await main_channel.edit(name=str("Closed-" + str(main_channel.name)))

                del order_ext_list[int(index-2):int(index+3)]

                order_ext_file = open("order_ext.list", "w")
                for order in order_ext_list: 
                    order_ext_file.write(str(order + "\n"))
                order_ext_file.close()

                msg_ptrn = "<@!(.*?)>"
                user_id = re.search(msg_ptrn, message.content)
                user = message.guild.get_member(int(user_id.group(1)))
                await channel.set_permissions(user, read_messages=True, send_messages=False)

client.run(os.getenv('TOKEN'))

