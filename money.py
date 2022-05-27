from setting import *
from functions import *

# bring changes to how much money each server earned
def addMoney(data, server):
    # updates amount of money in airtable
    for serverIDGET in range(len(data["records"])):
        serverID1 = str(data["records"][serverIDGET]["fields"]["guild_id"])
        serverID = serverID1 + str(data["records"][serverIDGET]["fields"]["guild_id2"])
        if serverID == server:
            record_id = data["records"][serverIDGET]["id"]
            current_money = data["records"][serverIDGET]["fields"]["earned"]
            break
        else:
            pass
    # a small fix to get rid of some errors - just need to organize the loop better and use a better search algo
    money = current_money + 0.01
    updateData(serverID1, 0, money, record_id)