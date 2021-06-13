#import discord

from decode_container import parse_container
#from calculators.main_calculator_handler import calculate_container
from calculators_dev.main_calculator_handler import calculate_container
from utils import human_number as hf, get_data, get_storage


test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}
                  #Zap breaks it, but why?

user = 0
username = test_usernames[user]

# Parse/Grab data
player_data, other_data = get_data(username)

# For testing:
inv_contents, talisman_bag, ender_chest, armour, wardrobe, personal_vault, storage_items, pet_items = ([],[],[],[],[],[],[],[])
inventory_worth, accessories_worth, ender_chest_worth, armour_worth, wardrobe_worth, vault_worth, storage_worth, pets_worth = (0, 0, 0, 0, 0, 0, 0, 0)

# Get item groupings
inv_contents   = parse_container(player_data.get("inv_contents", {"data": []})['data'])
talisman_bag   = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
#'''
ender_chest    = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
armour         = parse_container(player_data.get("inv_armor", {"data": []})['data'])
wardrobe       = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
storage_items  = get_storage(player_data)
pet_items      = player_data.get("pets", [])
#'''

# Calculate each section
inventory_worth   = calculate_container(inv_contents[:5])#, print_prices=True)
#'''
accessories_worth = calculate_container(talisman_bag)#, print_prices=True)
ender_chest_worth = calculate_container(ender_chest)#, print_prices=True)
armour_worth      = calculate_container(armour)#, print_prices=True)
wardrobe_worth    = calculate_container(wardrobe)#, print_prices=True)
vault_worth       = calculate_container(personal_vault)#, print_prices=True)
storage_worth     = calculate_container(storage_items)#, print_prices=True)
pets_worth        = calculate_container(pet_items)#, print_prices=True)
#'''
# Other sections
purse = int(player_data.get("coin_purse", 0))  # For some reason, purse contains a bunch of extra decimal places.
banking = int(other_data.get("banking", {"balance": 0}).get("balance", 0))  # Same with Bank

# Total
total = sum([purse, banking, pets_worth, inventory_worth, accessories_worth, ender_chest_worth,
             armour_worth, wardrobe_worth, vault_worth, storage_worth])

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
