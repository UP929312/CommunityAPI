import discord
import json
import requests

with open("api_key.txt", 'r') as file:
    API_KEY = file.read()

from decode_container import parse_container
from calculators.main_calculator_handler import calculate_container
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
    for i in range(1, 19):
        page = player_data["backpack_contents"].get(str(i), {"data": []})
        storage_items.extend(parse_container(page["data"]))
    return storage_items

# Setup
#username = "56ms"  # ------------------
username = "nonbunary"
#username = "Poroknights"
#username = "UrMinecraftDoggo"
#username = "Skezza"
#username = "Refraction"
username = "seattle72"

# Parse/Grab data
player_data, other_data = get_data(username)

# For testing:
accessories_worth, inventory_worth, ender_chest_worth, armour_worth, wardrobe_worth, vault_worth, storage_worth, pets_worth = (0, 0, 0, 0, 0, 0, 0, 0)

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
accessories_worth = calculate_container(talisman_bag, print_prices=True)
inventory_worth   = calculate_container(inv_contents)#, print_prices=True)
ender_chest_worth = calculate_container(ender_chest)#, print_prices=True)
armour_worth      = calculate_container(armour)#, print_prices=True)
wardrobe_worth    = calculate_container(wardrobe)#, print_prices=True)
vault_worth       = calculate_container(personal_vault)#, print_prices=True)
storage_worth     = calculate_container(storage_items)#, print_prices=True)
pets_worth        = calculate_container(pet_items, print_prices=True)

# Other sections
purse = int(player_data.get("coin_purse", 0))  # For some reason, purse contains a bunch of extra decimal places.
banking = int(other_data.get("banking", {"balance": 0}).get("balance", 0))  # Same with Bank

#'''
# Total
total = purse+banking+pets_worth+inventory_worth+accessories_worth+ender_chest_worth+armour_worth+wardrobe_worth+vault_worth+storage_worth

data = [f"Purse: {hf(purse)}",
        f"Bank: {hf(banking)}",
        f"Pets: {hf(pets_worth)}",
        f"Inventory: {hf(inventory_worth)}",
        f"Accessories: {hf(accessories_worth)}",
        f"Ender chest: {hf(ender_chest_worth)}",
        f"Armor worth: {hf(armour_worth)}",
        f"Wardrobe: {hf(wardrobe_worth)}",
        f"Personal vault: {hf(vault_worth)}",
        f"Storage: {hf(storage_worth)}",
        f"Total = {hf(total)}"]

print("\n".join(data))
#'''
