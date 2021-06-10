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
    print('reaction_roles started on bot {0.user}'.format(client))

@client.listen()
async def on_raw_reaction_add(payload):
    if payload.channel_id == int(os.getenv('roles_chan')):
        if payload.message_id == int(os.getenv('roles_msg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)

            buyer = discord.utils.get(message.guild.roles, name=str(os.getenv('buyer_role')))
            seller = discord.utils.get(message.guild.roles, name=str(os.getenv('seller_role')))
            advertiser = discord.utils.get(message.guild.roles, name=str(os.getenv('advertiser_role')))

            if str(payload.emoji) == str(os.getenv('buyer_emote')):
                if buyer not in user.roles:
                    print(user, "requested the role Buyer")
                    await user.add_roles(buyer)
    
            elif str(payload.emoji) == str(os.getenv('seller_emote')):
                if seller not in user.roles:
                    print(user, "requested the role Seller")
                    await user.add_roles(seller)
    
            elif str(payload.emoji) == str(os.getenv('advertiser_emote')):
                if advertiser not in user.roles:
                    print(user, "requested the role Advertiser")
                    await user.add_roles(advertiser)
            else:
                await message.remove_reaction(payload.emoji, payload.member)

@client.listen()
async def on_raw_reaction_remove(payload):
    if payload.channel_id == int(os.getenv('roles_chan')):
        if payload.message_id == int(os.getenv('roles_msg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)
            
            buyer = discord.utils.get(message.guild.roles, name=str(os.getenv('buyer_role')))
            seller = discord.utils.get(message.guild.roles, name=str(os.getenv('seller_role')))
            advertiser = discord.utils.get(message.guild.roles, name=str(os.getenv('advertiser_role')))

            if str(payload.emoji) == str(os.getenv('buyer_emote')):
                if buyer in user.roles:
                    print(user, "requested the role Buyer")
                    await user.remove_roles(buyer)
    
            elif str(payload.emoji) == str(os.getenv('seller_emote')):
                if seller in user.roles:
                    print(user, "requested the role Seller")
                    await user.remove_roles(seller)
    
            elif str(payload.emoji) == str(os.getenv('advertiser_emote')):
                if advertiser in user.roles:
                    print(user, "requested the role Advertiser")
                    await user.remove_roles(advertiser)
    
client.run(os.getenv('TOKEN'))

