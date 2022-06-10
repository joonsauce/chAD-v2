from setting import *
from money import *

# ML code to analyze contents of the message - will be written soon
def anamsg(msg):
    return

# get random ad from most relevant topic the server is interested in
def getAd(id):
    # get information about the server
    svr_info = getSvrInfo(id)
    # get ad related to what the server wants
    data = getData(svr_info)

# get information about the server
def getSvrInfo(svr_id):
    # split server ID into two parts
    svr = str(svr_id)
    svr_id_1 = svr[:8]
    svr_id_2 = svr[8:]
    # get information from the database
    url = api_link
    response = requests.get(url=url, headers=header1, params=params)
    if response != 200:
        return -1
    data = response.json()
    servers = list(map(lambda x: x, data["records"]))
    # if svr_id_1 in servers:


# everything below is the old code - some code will be recycled

# gets a random ad to display - will be partially rewritten in the near future
def getRandomAtt():
    data = getData(False)
    x = len(data["records"])
    num = randint(0, x)
    return data["records"][num]["fields"]

# uses the random ad from above to send into the servers through Discord embeds
def sendAD(svr_id):
    # code below updates the amount of revenue generated in the server
    data = getData(True)
    addMoney(data, svr_id)
    # code below creates embed to send the ad
    embed = discord.Embed(color=discord.Colour.dark_red())
    # get information about ad to show
    ad = getRandomAtt()
    embed.set_author(name="Advertisement from {}".format(ad["compName"]))
    embed.set_image(url=ad["imgLink"])
    embed.add_field(name='{}'.format(ad["compName"]),
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
