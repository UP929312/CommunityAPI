import requests

from data.decode_container import parse_container
from exceptions import InvalidApiKeyException, InvalidUsername, MojangServerError

with open("data/hypixel_api_key.txt", 'r') as file:
    API_KEY = file.read()
#=======================================================


def get_data(username):
   
    if len(username) <= 16:
        uuid_request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        # For invalid usernames, the uuid_request.text will be ''
        if not uuid_request.text:
            raise InvalidUsername
        # For mojang's servers being down
        if uuid_request.status_code != 200:
            raise MojangServerError
        uuid = uuid_request.json()["id"]
    else:
        uuid = username.replace("-", "")
    
    profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
    
    if profile_list == {'success': False, 'cause': 'Invalid API key'}:
        print("Data/utils: Invalid API key...?")
        raise InvalidApiKeyException
    
    if not profile_list or profile_list.get("profiles") is None or profile_list == {'success': True, 'profiles': None}:
        print("# Error, profile parsing error. Possible wrong username?")
        raise InvalidUsername
    
    try:         
        valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]        
        profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
        player_data = profile["members"][uuid]; other_data = profile
    except Exception as e:
        print("######", e)
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
