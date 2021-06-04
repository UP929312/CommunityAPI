import discord
import json
import requests

with open("api_key.txt", 'r') as file:
    API_KEY = file.read()

from decode_container import parse_container


def get_data(username):
    try:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]
        
        profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
        valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]
        profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
        player_data = profile["members"][uuid]; other_data = profile
    except:
        return None, None
    return player_data, other_data


# Setup
username = "Poroknights"  # ------------------
# Parse/Grab data
player_data, other_data = get_data(username)

# Get item groupings
inv_contents = parse_container(player_data.get("inv_contents", {"data": []})['data'])
talisman_bag   = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
inv_contents   = parse_container(player_data.get("inv_contents", {"data": []})['data'])
ender_chest    = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
armour         = parse_container(player_data.get("inv_armor", {"data": []})['data'])
wardrobe       = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
#storage_items  = get_storage(player_data)
#pet_items      = player_data.get("pets", [])

print(inv_contents[0].__nbt__)
