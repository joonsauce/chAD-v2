from setting import *
from money import *

# gets a random ad to display - will be partially rewritten in the near future
def getRandomAtt():
    data = getData("ads")
    x = len(data["records"])
    num = randint(0, x)
    return data["records"][num]["fields"]

# uses the random ad from above to send into the servers through Discord embeds
def sendAD(svr_id):
    # code below updates the amount of revenue generated in the server
    data = getData(True)
    addMoney(svr_id)
    # code below creates embed to send the ad
    embed = discord.Embed(color=discord.Colour.dark_red())
    # get information about ad to show
    ad = getRandomAtt()
    embed.set_author(name="Advertisement from {}".format(ad["compName"]))
    embed.set_image(url=ad["imgLink"])
    embed.add_field(name='What is {}?'.format(ad["compName"]),
                    value=ad["msgFromSponsor"] + " " + ad["link2sponsor"],
                    inline=False)
    return embed

# differentiates between the two types of tables
def getData(type):
    if type:
        url = api_link
    else:
        url = api_link2
    response = requests.get(url=url, headers=header1, params=params)
    print("Get Response: " + str(response))
    data = response.json()
    return data

# updates the data in the airtable
def updateData(serverID1, type, value, record_id):
    if type == 0:
        data = '{"fields": { "guild_id": ' + str(serverID1) + ', "plan_type": ' + str(value) + '}}'
    else:
        data = '{"fields": { "guild_id": ' + str(serverID1) + ', "text_count": ' + str(value) + '}}'

    url = api_link + str(record_id)
    response = requests.patch(url=url,
                              headers=header2,
                              data=data)
    print("Update Response: " + str(response))
