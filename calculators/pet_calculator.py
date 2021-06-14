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
    
def calculate_pet(price, print_prices):

    pet = price.item
    value = price.value
    
    pet_level = get_pet_level(pet)

    #######################################################################################
    # BASE VALUE
    if f"{pet['type']};{TIERS.index(pet['tier'])}" in LOWEST_BIN:
        # Try from LOWEST_BIN
        value["base_price"] = LOWEST_BIN[f"{pet['type']};{TIERS.index(pet['tier'])}"]
        value["price_source"] = "BIN"
    else:
        # Try from Jerry's list
        value["base_price"] = PRICES.get(f"LVL_1_{pet['tier']}_{pet['type']}", 0)  # LVL_1_COMMON_ENDERMAN
        value["price_source"] = "Jerry's List"

    #######################################################################################
    # PET ITEM VALUE
    pet_held_item = pet.get("heldItem", "")
    if pet_held_item:
        value["held_item"] = {}
        value["held_item"]["value"] = LOWEST_BIN.get(pet_held_item, 0)
        value["held_item"]["price_source"] = "BIN"
        
    #######################################################################################
    # PET SKIN VALUE
    pet_skin = pet.get("skin", False)
    if pet_skin:
        value["pet_skin"] = {}
        value["pet_skin"]["value"] = LOWEST_BIN.get("PET_SKIN_"+pet['skin'], 0)
        value["pet_skin"]["price_source"] = "BIN" if pet_skin else "Unknown"

    #######################################################################################

    # PET LEVEL BONUS
    pet_level_bonus = int(pet["exp"]*COINS_PER_XP)  # 5 Xp = 1 coin, seems about right but this is subjective.

    value["pet_level_bonus"] = {}
    value["pet_level_bonus"]["amount"] = f"{int(pet['exp'])} xp"
    value["pet_level_bonus"]["worth"] = pet_level_bonus

    #######################################################################################

    price.value = value
    return price
