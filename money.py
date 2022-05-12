from setting import *
from functions import *

# bring changes to how much money each server earned
def updateMoney(data, id):
    # updates amount of money in airtable
    for serverIDGET in range(len(data["records"])):
        serverID1 = str(data["records"][serverIDGET]["fields"]["guild_id"])
        serverID = serverID1 + str(data["records"][serverIDGET]["fields"]["guild_id2"])
        if serverID == id:
            record_id = data["records"][serverIDGET]["id"]
            current_count = data["records"][serverIDGET]["fields"]["text_count"]
            break
        else:
            pass
    # will be obsolete - idek what this accomplishes
    countUpdate = current_count + 1
    # will be obsolete - will be rewritten & function changed
    updateData(serverID1, 1, countUpdate, record_id)