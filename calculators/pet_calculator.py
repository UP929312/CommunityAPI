from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN
from constants.pets import PET_DICT

TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]
#print([(TIERS.index(x), x) for x in TIERS])
COINS_PER_XP = 0.2

def get_pet_level(pet):
    #print("-"*50)
    pet_tier = pet["tier"] if pet["tier"] != "MYTHIC" else "LEGENDARY"
    pet_xp = pet["exp"]
    xp_offset = PET_DICT["pet_rarity_offset"][pet_tier]
    
    pet_level = 1
    while pet_xp > 0 and pet_level < 99:
        pet_xp -= PET_DICT['pet_levels'][pet_level+xp_offset]
        pet_level += 1

    if len(PET_DICT['pet_levels']) == (pet_level+xp_offset):  # Edge case for level 100s (There is no xp required when ranking up to Level 101
        return 100

    return pet_level
    
    
def calculate_pet(pet, print_prices):
    pet_level = get_pet_level(pet)    

    if f"{pet['type']};{TIERS.index(pet['tier'])}" in LOWEST_BIN:
        # Try from LOWEST_BIN
        base_pet_price = LOWEST_BIN[f"{pet['type']};{TIERS.index(pet['tier'])}"]
    else:
        # Try from Jerry's list
        level = 100 if pet_level >= 100 else 1
        base_pet_price = PRICES.get(f"LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()}", 0)  # LVL_x_COMMON_ENDERMAN
        #print(f"Pet at LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()} priced at {price}")

    pet_held_item = pet.get("heldItem", "")
    held_item_price = LOWEST_BIN.get(pet_held_item, 0)
    pet_level_bonus = int(pet["exp"]*COINS_PER_XP)  # 5 Xp = 1 coin, seems about right but this is subjective.

    if print_prices:
        print(f"{pet['type']} ({pet['tier']}) with level {pet_level}")
        print(f"Total estimated value: {base_pet_price+pet_level_bonus+held_item_price}, made up of Base: {base_pet_price}, Held item ({pet_held_item}): {held_item_price} and {pet_level_bonus} level bonus.")
    return base_pet_price+pet_level_bonus+held_item_price
