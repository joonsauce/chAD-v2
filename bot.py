from functions import *
from setting import *

# main function - will be massively overhauled in the near future
@bot.event
async def on_message(message):
    # this way bot sending something doesn't trigger anything
    if message.author.bot:
        pass
    else:
        server_id = str(message.guild.id)
        if server_id in text_counts.keys():
            count = int(text_counts.get(server_id))
            count += 1
            data = getData("ud")
            # updates amount of money in airtable
            for serverIDGET in range(len(data["records"])):
                serverID1 = str(data["records"][serverIDGET]["fields"]["guild_id"])
                serverID = serverID1 + str(data["records"][serverIDGET]["fields"]["guild_id2"])
                if serverID == server_id:
                    record_id = data["records"][serverIDGET]["id"]
                    current_count = data["records"][serverIDGET]["fields"]["text_count"]
                    break
                else:
                    pass
            # will be obsolete - idek what this accomplishes
            countUpdate = current_count + 1
            # will be obsolete - will be rewritten & function changed
            updateData(serverID1, 1, countUpdate, record_id)
        else:
            count = 1
            text_counts.setdefault(server_id, count)
            print(1)

        # will be changed up soon - counted number of messages necessary to get an ad & earn money
        # numberOfPeople = bot.get_guild(message.guild.id)
        # maxThreshold = numberOfPeople * 30

        # if count > maxThreshold:
            # ans = sendAD()
            # await message.channel.send(embed=ans)
            # text_counts.update({server_id: 0})
            # addMoney(server_id)
            # updateData(serverID1, 2, 0, record_id)
        # else:
            # text_counts.update({server_id: count})

bot.run(discord_token)
