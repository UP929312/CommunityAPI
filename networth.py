#import discord

from decode_container import parse_container
from calculators.main_calculator_handler import calculate_container
from utils import human_number as hf, get_data, get_storage

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}
                  #Zap breaks it, but why?

user = 0#6#8
username = test_usernames[user]

# Parse/Grab data
player_data, other_data = get_data(username)

# For testing:
inv_contents, talisman_bag, ender_chest, armour, wardrobe, personal_vault, storage_items, pet_items = ([],[],[],[],[],[],[],[])
inventory_worth, accessories_worth, ender_chest_worth, armour_worth, wardrobe_worth, vault_worth, storage_worth, pets_worth = (0, 0, 0, 0, 0, 0, 0, 0)

# Get item groupings
inv_contents   = parse_container(player_data.get("inv_contents", {"data": []})['data'])
#'''
talisman_bag   = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
ender_chest    = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
armour         = parse_container(player_data.get("inv_armor", {"data": []})['data'])
wardrobe       = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
storage_items  = get_storage(player_data)
pet_items      = player_data.get("pets", [])
#'''

# Calculate each section
inventory_worth   = calculate_container(inv_contents)#, print_prices=True) # [:5]
#'''
accessories_worth = calculate_container(talisman_bag)#, print_prices=True)
ender_chest_worth = calculate_container(ender_chest)#, print_prices=True)
armour_worth      = calculate_container(armour)#, print_prices=True)
wardrobe_worth    = calculate_container(wardrobe)#, print_prices=True)
vault_worth       = calculate_container(personal_vault)#, print_prices=True)
storage_worth     = calculate_container(storage_items)#, print_prices=True)
pets_worth        = calculate_container(pet_items)#, print_prices=True)
#'''

inventory_total   = sum(x.calculate_total() for x in inventory_worth)
accessories_total = sum(x.calculate_total() for x in accessories_worth)
ender_chest_total = sum(x.calculate_total() for x in ender_chest_worth)
armour_total      = sum(x.calculate_total() for x in armour_worth)
wardrobe_total    = sum(x.calculate_total() for x in wardrobe_worth)
vault_total       = sum(x.calculate_total() for x in vault_worth)
storage_total     = sum(x.calculate_total() for x in storage_worth)
pets_total        = sum(x.calculate_total() for x in pets_worth)

# Other sections
purse = int(player_data.get("coin_purse", 0))  # For some reason, purse contains a bunch of extra decimal places.
banking = int(other_data.get("banking", {"balance": 0}).get("balance", 0))  # Same with Bank

# Total
total = sum([purse, banking, inventory_total, accessories_total, ender_chest_total, armour_total,
             wardrobe_total, vault_total, storage_total, pets_total])

data = ["="*10,
        f"Purse: {hf(purse)}",
        f"Bank: {hf(banking)}",
        f"Pets: {hf(pets_total)}",
        f"Inventory: {hf(inventory_total)}",
        f"Accessories: {hf(accessories_total)}",
        f"Ender chest: {hf(ender_chest_total)}",
        f"Armor worth: {hf(armour_total)}",
        f"Wardrobe: {hf(wardrobe_total)}",
        f"Personal vault: {hf(vault_total)}",
        f"Storage: {hf(storage_total)}",
        f"Total = {hf(total)}"]

print("\n".join(data))

#print("Top inventory items = ")
#for price in sorted(inventory_worth, key=lambda x: x.total, reverse=True)[:5]:
#    print(price.item.internal_name, price.total)
