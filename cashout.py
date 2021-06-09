#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import mysql.connector

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
    print('!cashout started on bot {0.user}'.format(client))


@client.command()
async def cashout(ctx, user: discord.Member):
    if ctx.channel.category_id == int(os.getenv('payout_cat')):
        mycursor.execute(str("SELECT date, buyer, amount FROM commissions WHERE id=" + str(user.id)))
        commissions = mycursor.fetchall()

        if not commissions:
            await ctx.send("<@!" + str(user.id) + "> has no available commissions.")
        else:
            mycursor.execute("DELETE FROM commissions WHERE id=" + str(user.id))
            mydb.commit()
            await ctx.send("<@!" + str(user.id) + "> has been marked as cashed out for all available commissions.")
    
    else:
        await ctx.send("You must use this command in a payout channel")


'''@cashout.error
async def cashout_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @User to cashout")'''

client.run(os.getenv('TOKEN'))
