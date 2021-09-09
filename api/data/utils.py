import aiohttp

from data.decode_container import parse_container
from exceptions import InvalidApiKeyException, InvalidUsername, MojangServerError

with open("data/hypixel_api_key.txt", 'r') as file:
    API_KEY = file.read()

async def async_conversion(session, url):
    async with session.get(url) as request:
        try:
            json = await request.json()
        except:
            request.text = ''
            return "", request 
        return json, request

async def async_request(session, url):
    async with session.get(url) as request:
        return await request.json()

#=======================================================

async def get_data(session, username):
   
    if len(username) <= 16:
        json, request = await async_conversion(session, f"https://api.mojang.com/users/profiles/minecraft/{username}")
        # For invalid usernames, the request.text will be ''
        if not request.text:
            raise InvalidUsername
        # For mojang's servers being down
        if request.status != 200:
            raise MojangServerError
        uuid = json["id"]
    else:
        uuid = username.replace("-", "")

    profile_list = await async_request(session, f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}")
    
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
