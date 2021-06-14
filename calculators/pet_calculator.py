from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN
from constants.pets import PET_LEVELS

RARITY_OFFSET = {"COMMON": 0, "UNCOMMON": 6, "RARE": 11, "EPIC": 16, "LEGENDARY": 20, "MYTHIC": 20}
TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]

COINS_PER_XP = 0.2

def get_pet_level(pet):
    pet_xp = pet["exp"]
    xp_offset = RARITY_OFFSET[pet["tier"]]
    
    pet_level = 1  
    while pet_xp > 0 and pet_level < 100:
        pet_xp -= (PET_LEVELS+[5000000000000])[pet_level+xp_offset]
        pet_level += 1

    return pet_level    
    
def calculate_pet(pet, print_prices):
    pet_level = get_pet_level(pet)

    if f"{pet['type']};{TIERS.index(pet['tier'])}" in LOWEST_BIN:
        # Try from LOWEST_BIN
        base_pet_price = LOWEST_BIN[f"{pet['type']};{TIERS.index(pet['tier'])}"]
    else:
        # Try from Jerry's list
        base_pet_price = PRICES.get(f"LVL_1_{pet['tier']}_{pet['type']}", 0)  # LVL_1_COMMON_ENDERMAN

    pet_held_item = pet.get("heldItem", "")
    held_item_price = LOWEST_BIN.get(pet_held_item, 0)
    pet_level_bonus = int(pet["exp"]*COINS_PER_XP)  # 5 Xp = 1 coin, seems about right but this is subjective.

    pet_skin_price = LOWEST_BIN.get("PET_SKIN_"+pet['skin'], 0) if pet.get("skin", None) is not None else 0

    total = base_pet_price+pet_level_bonus+held_item_price+pet_skin_price

    if print_prices:# and total > 50_000_000:
        print(f"{pet['type']} ({pet['tier']}) with level {pet_level}")
        print(f"Total estimated value: {base_pet_price+pet_level_bonus+held_item_price+pet_skin_price}, made up of Base: {base_pet_price}, Held item ({pet_held_item}): {held_item_price}, Level {pet_level_bonus} bonus and Skin price: {pet_skin_price}.")
    return total
