from setting import *
from functions import *

# bring changes to how much money each server earned
def addMoney(server):
    data = getData(True)
    # updates amount of money in airtable
    for serverIDGET in range(len(data["records"])):
        serverID1 = str(data["records"][serverIDGET]["fields"]["guild_id"])
        serverID = serverID1 + str(data["records"][serverIDGET]["fields"]["guild_id2"])
        if serverID == server:
            record_id = data["records"][serverIDGET]["id"]
            current_money = data["records"][serverIDGET]["fields"]["plan_type"]
            break
        else:
            pass
    money = current_money + 0.01
    updateData(serverID1, 0, money, record_id)