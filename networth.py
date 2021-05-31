import discord
import json
import requests

with open("api_key.txt", 'r') as file:
    API_KEY = file.read()

from decode_container import parse_container
from calculators import calc_pets, calc_stars, calculate_items
from utils import human_number as hf

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

def get_storage(player_data):
    storage_items = []
    for i in ("1", "2", "3", "4"):
        page = player_data["backpack_contents"].get(i, {"data": []})
        storage_items.extend(parse_container(page["data"]))
    return storage_items

# Setup
username = "nonbunary"  # ------------------

# Parse/Grab data
player_data, other_data = get_data(username)

# Get item groupings
talisman_bag   = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
inv_contents   = parse_container(player_data.get("inv_contents", {"data": []})['data'])
ender_chest    = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
armour         = parse_container(player_data.get("inv_armor", {"data": []})['data'])
wardrobe       = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
storage_items  = get_storage(player_data)
pet_items      = player_data.get("pets", [])

# Calculate each section
accessories_worth = calculate_items(talisman_bag)
inventory_worth   = calculate_items(inv_contents)
ender_chest_worth = calculate_items(ender_chest)
armour_worth      = calculate_items(armour)
wardrobe_worth    = calculate_items(wardrobe, print_prices=True)
vault_worth       = calculate_items(personal_vault)
storage_worth     = calculate_items(storage_items)

# Other sections
purse = int(player_data.get("coin_purse", 0))  # For some reason, purse contains a bunch of extra decimal places.
banking = int(other_data.get("banking", {"balance": 0}).get("balance", 0))  # Same with Bank
pets = calc_pets(pet_items)

# Total
total = purse+banking+pets+inventory_worth+accessories_worth+ender_chest_worth+armour_worth+wardrobe_worth+vault_worth+storage_worth

data = [f"Purse: {hf(purse)}",
        f"Bank: {hf(banking)}",
        f"Pets: {hf(pets)}",
        f"Inventory: {hf(inventory_worth)}",
        f"Accessories: {hf(accessories_worth)}",
        f"Ender chest: {hf(ender_chest_worth)}",
        f"Armor worth: {hf(armour_worth)}",
        f"Wardrobe: {hf(wardrobe_worth)}",
        f"Personal vault: {hf(vault_worth)}",
        f"Storage: {hf(storage_worth)}",
        f"Total = {hf(total)}"]

print("\n".join(data))