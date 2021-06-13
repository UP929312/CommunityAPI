import requests
from math import log10

from decode_container import parse_container

with open("api_key.txt", 'r') as file:
    API_KEY = file.read()

#=======================================================

def get_data(username):
    try:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]
        
        profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
        valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]
        profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
        player_data = profile["members"][uuid]; other_data = profile
    except Exception as e:
        print(e)
        return None, None
    return player_data, other_data

def get_storage(player_data):
    storage_items = []
    if not player_data.get("backpack_contents", False):
        return []
    for i in range(0, 19):
        page = player_data["backpack_contents"].get(str(i), {"data": []})
        storage_items.extend(parse_container(page["data"]))
    return storage_items

#=======================================================

letter_values = {"": 1,
                 "K": 1000,
                 "M": 1000000,
                 "B": 1000000000}

ends = list(letter_values.keys())

def human_number(num):
    '''
    Takes an int/float e.g. 10000 and returns a formatted version e.g. 10k
    '''

    if isinstance(num, str):
        return num
    
    if num < 1: return 0

    rounded = round(num, 3 - int(log10(num)) - 1)
    suffix = ends[int(log10(rounded)/3)]
    new_num = str(rounded / letter_values[suffix])
    if new_num.endswith(".0"):
        new_num = new_num[:-2]
    return str(new_num)+suffix



