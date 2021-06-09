#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import asyncio
import mysql.connector
from tabulate import tabulate

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv('db_password'),
    database="burnt_bot"
)

mycursor = mydb.cursor()

@client.event
async def on_ready():
    print('payout started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    if payload.channel_id == int(os.getenv('payout_chan')):
        if payload.message_id == int(os.getenv('payout_msg')):
            channel = client.get_channel(payload.channel_id)
            await asyncio.sleep(0.3)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)
            if str(payload.emoji.name) == "📩":
                user = message.guild.get_member(payload.user_id)
                category = client.get_channel(int(os.getenv('payout_cat')))

                index_file = open("payout.index", "r")
                index = index_file.readlines()
                index_file.close()

                index = len(index) + 1
                        
                index_file = open("payout.index", "a")
                index_file.write(str(str(index) + "\n"))
                index_file.close()

                payout_chan = await message.guild.create_text_channel(str("Payout-" + str(index)), category=category)
                await payout_chan.set_permissions(user, read_messages=True, send_messages=True)

                payout_file = open("payout.msg", "r")
                payout_message = await payout_chan.send("Hey <@!" + str(user.id) + ">, you have created a new payout request.\n\n" + str(payout_file.read()))
                payout_file.close()

                list_file = open("payout.list", "a")
                list_file.write(str(str(payout_message.id) + "\n"))
                list_file.close()

                await payout_message.add_reaction("🔒")
                await payout_message.pin()

                mycursor.execute(str("SELECT date, buyer, amount FROM commissions WHERE id=" + str(user.id)))
                commissions = mycursor.fetchall()

                title = ("Date", "Buyer", "Commission")
            
                if not commissions:
                    await payout_chan.send("You have no unpaid commissions available.")
                else:
                    total=0
                    for commission in commissions:
                        total=total+int(commission[2])

                    await payout_chan.send("Uncashed commissions:\n```" + str((tabulate(commissions, title, tablefmt="orgtbl"))) + "```\n\nTotal available uncashed commission: " + str(total))

                
client.run(os.getenv('TOKEN'))

