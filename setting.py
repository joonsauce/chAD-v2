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
    svr_list = list(map(grab_svr, data['records']))
    # stops ready procedure if all servers are already registered
    if all(servers) in svr_list:
        return
    new_list = numpy.subtract(servers, svr_list)
    for svr in new_list:
        svr1 = svr[8:]
        svr2 = svr[:8]
        data = '{ "records": [ { "fields": { "guild_id": ' + str(svr1) + ', "guild_id2": ' + str(
            svr2) + ', "plan_type": ' + str(0) + '} }] }'
        response = requests.post(url=api_link, headers=header1, data=data)
        if response != 200:
            print("Server list update error")
            exit()
    print("Status: Ready")

# old code is below - need to change startup behavior

# start up procedure for bot
@bot.event
async def on_ready():
    # changes bot status
    await bot.change_presence(activity=discord.Game("The better way to advertise"))
    # whatever is below needs to be largely rewritten - deleting servers and re-adding them is just inefficient
    # below contacts airtable to edit the tables
    servers = bot.guilds
    # GETs all records in the table to check if all servers bot is in, is in the table
    response = requests.get(url=api_link,
                            headers=header1,
                            params=params)
    print("Get Response: " + str(response))
    data = response.json()
    for u in range(len(data["records"])):
        planid = str(data["records"][u]["fields"]["guild_id"]) + str(data["records"][u]["fields"]["guild_id2"])
        plan_types.update({str(planid): data["records"][u]["fields"]["plan_type"]})
        text_counts.update({str(planid): data["records"][u]["fields"]["text_count"]})
    # DELETEs all records to replace with the updated set of servers
    for k in range(len(data["records"])):
        records = data["records"][k]["id"]

        response = requests.delete(url=api_link + records,
                                   headers=header1)
        print("Delete Reponse: " + str(response))

    # POSTs updated list of servers the bot is in
    for i in range(len(servers)):
        # have to split the server id into two parts because Airtable couldn't handle longer integers
        id = list(str(servers[i].id))
        idsplit1 = []
        idsplit2 = []
        for p in range(len(id)):
            if p <= 8:
                idsplit1.append(id[p])
            else:
                idsplit2.append(id[p])
        id1 = str()
        id2 = str()
        for r in range(len(idsplit1)):
            id1 = id1 + idsplit1[r]
            id2 = id2 + idsplit2[r]
        id = id1 + id2
        plan = plan_types.get(str(id))
        text = text_counts.get(str(id))
        if not plan:
            plan = 0
        else:
            pass
        if not text:
            text = 0
        else:
            pass

        data = '{ "records": [ { "fields": { "guild_id": ' + str(id1) + ', "guild_id2": ' + str(id2) + ', "plan_type": ' + str(plan) + ', "text_count": ' + str(text) + '} }] }'


        response = requests.post(url=api_link,
                                 headers=header2,
                                 data=data)
        print("Post Response: " + str(response))
    # returns updated version of the table
    response = requests.get(url=api_link,
                            headers=header1,
                            params=params)
    print("Get Response: " + str(response))
    data = response.json()
    for finalGET in range(len(servers)):
        records1 = str(data["records"][finalGET]["fields"]["guild_id"])
        records2 = str(data["records"][finalGET]["fields"]["guild_id2"])
        records = records1 + records2
    # prints that the bot is ready to go
    print("Status: OK")
