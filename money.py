from setting import *
from functions import *

# bring changes to how much money each server earned
def addMoney(svr_id):
    url = api_link
    response = requests.get(url=url, headers=header1, params=params)
    data = response.json()
    def grab_svr(data):
        return data["fields"]["guild_id"]
    servers = list(map(grab_svr, data["records"]))
    if str(svr_id)[8:] in servers:
        record_id = data["records"][str(svr_id)[8:]]["id"]
        money = data["records"][str(svr_id)[8:]]["id"]
    else:
        return
    updateData(str(svr_id)[8:], 0, float(money) + 0.01, record_id)