#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import re
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
    print('welcome started on bot {0.user}'.format(client))


@client.event
async def on_member_join(member):
    if member.guild.id != int(os.getenv('main_server')):
        return

    code_ptrn = "<code=(.*?)>"
    inviter_ptrn = "<inviter=(.*?)>"
    uses_ptrn = "<uses=(.*?)>"

    new_invites = await member.guild.invites()

    invites_file = open("invites.index", "r")
    old_invites = invites_file.readlines()
    invites_file.close()
    old_invites = list(map(str.strip, old_invites))

    invites_file = open("invites.index", "w")
    for invite in new_invites:
        invites_file.write(str(str(invite.code) + "\n"))
        invites_file.write(str(str(invite.uses) + "\n"))
    invites_file.close()

    for invite in new_invites:
        try:
            old_index = int(old_invites.index(str(invite.code)))
        except:
            break

        if invite.uses > int(old_invites[int(old_index+1)]):
            break

    buyer = discord.utils.get(member.guild.roles, name="Buyer")
    await member.add_roles(buyer)

    channel = client.get_channel(int(os.getenv('welcome_chan')))
    await channel.send("Hey <@!" + str(member.id) + ">, welcome to " + member.guild.name + "\n\nTo place an order use <#" + os.getenv('order_chan') + ">.\nTo create a ticket use <#" + os.getenv('ticket_chan') + ">.\n\nI have detected that you were invited by <@!" + str(invite.inviter.id) + ">. If this seems incorrect, create a ticket to correct it.")

    mycursor = mydb.cursor()
    sql = "INSERT INTO buyers (date, name, id, inviter, inviter_id) VALUES (%s, %s, %s, %s, %s)"
    val = (str(datetime.now()), str(member), str(member.id), str(invite.inviter), str(invite.inviter.id))
    mycursor.execute(sql, val)
    mydb.commit()

client.run(os.getenv('TOKEN'))

