# import the api wrapper
import discord
# import to debug stuff - in case things aren't going well - not needed to run the bot
# import logging
# import to do some quick maths
import numpy
# import to check connections to the internet
import requests
# import to make some random stuff - will be obsolete in the future
import random
from random import seed
from random import randint
# import to gain access to bot commands
from discord.ext import commands
# import to gain access to API keys
from secrets import *
from collections import deque

# debug logger for bot - in case stuff is going wrong
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# sets prefix for bot - used for debug
prefix = "ad"

# sets description of the bot
description = "chAD-v2.00T"

# initializes bot
bot = commands.Bot(command_prefix=prefix)

# removes help command to add our own custom help command
bot.remove_command("help")

# defines text counts to count until bot + $1
text_counts = {}
plan_types = {}

# defines different header types for api calls
header1 = {
        'Authorization': 'Bearer {}'.format(api_key),
        }
header2 = {
            'Authorization': 'Bearer {}'.format(api_key),
            'Content-Type': 'application/json',
        }

# defines certain parameters for api calls
params = (
        ('maxRecords', 999),
        ('view', 'Grid view'),
    )

# bot startup procedure
@bot.event
async def on_ready():
    # set bot status
    await bot.change_presence(activity=discord.Game("chAD"))
    # checks the servers the bot is in - need to find a way for this function to be triggered whenever the bot joins a new server
    servers = bot.guilds
    # GET information from the airtable regarding which servers are registered
    response = requests.get(url=api_link, headers=header1, params=params)
    # if GET fails, stops the code (for now) - should trigger a backup code that can check if server up or not instead
    if response != 200:
        return
    # get the list of servers
    data = response.json()
    # grabs list of all the registered servers
    def grab_svr(data):
        return data["fields"]["guild_id"]
    # makes new list of all registered servers
    svr_list = list(map(grab_svr, data['records']))
    # stops ready procedure if all servers are already registered
    if all(servers) in svr_list:
        return
    # removes all already added servers and adds them to the list
    new_list = numpy.subtract(servers, svr_list)
    if any(new_list) not in servers:
        x_list = numpy.subtract(new_list, servers)
        new_new_list = numpy.subtract(new_list, x_list)
    else:
        new_new_list = new_list
    for svr in new_new_list:
        svr1 = svr[8:]
        svr2 = svr[:8]
        data = '{ "records": [ { "fields": { "guild_id": ' + str(svr1) + ', "guild_id2": ' + str(
            svr2) + ', "plan_type": ' + str(0) + '} }] }'
        response = requests.post(url=api_link, headers=header1, data=data)
        if response != 200:
            print("Server list update error")
            exit()
    print("Status: Ready")

# when bot joins a server, adds new server to database
@bot.event
async def on_guild_join(guild):
    svr = guild.id
    svr1 = svr[8:]
    svr2 = svr[:8]
    data = '{ "records": [ { "fields": { "guild_id": ' + str(svr1) + ', "guild_id2": ' + str(
        svr2) + ', "plan_type": ' + str(0) + '} }] }'
    response = requests.post(url=api_link, headers=header1, data=data)
    if response != 200:
        print("Server list update error")
        # need to run some error correcting so the bot can add the server to the database later (reciprocal)
        return
    await guild.system_channel.send("Please follow this link to activate chAD in your server:")