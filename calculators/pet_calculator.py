from constants.manual_price_checking_prices import PRICES as prices
from constants.lowest_bin import LOWEST_BIN
from constants.pets import PET_DICT

TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]
MAX_LEVELS = {"COMMON": 5_624_785, "UNCOMMON": 8_644_220, "RARE": 12_626_665, "EPIC": 18_608_500, "LEGENDARY": 25_353_230, "MYTHIC": 25_353_230}

def get_pet_level(pet):
    #print("-"*50)
    pet_tier = pet["tier"] if pet["tier"] != "MYTHIC" else "LEGENDARY"
    pet_xp = int(pet["exp"])
    xp_offset = PET_DICT["pet_rarity_offset"][pet_tier]
    
    pet_level = 1
    while pet_xp > 0 and pet_level < 99:
        pet_xp -= PET_DICT['pet_levels'][pet_level+xp_offset]
        pet_level += 1

    if len(PET_DICT['pet_levels']) == (pet_level+xp_offset):
        return 100, PET_DICT['pet_levels'][98+xp_offset]

    xp_required_at_pet_level = PET_DICT['pet_levels'][pet_level+xp_offset]

    return pet_level, xp_required_at_pet_level
    
    
def calculate_pet(pet):
    pet_level, xp_required = get_pet_level(pet)

    #print(f"{pet['type']} ({pet['tier']}) with level {pet_level}")

    # Try from LOWEST_BIN
    if f"{pet['type']};{TIERS.index(pet['tier'])}" in LOWEST_BIN:
        base_pet_price = LOWEST_BIN[f"{pet['type']};{TIERS.index(pet['tier'])}"]
    else:
        # Try from Jerry's list
        level = 100 if pet_level >= 100 else 1
        base_pet_price = prices.get(f"LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()}", 0)  # LVL_x_COMMON_ENDERMAN
        #print(f"Pet at LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()} priced at {price}")

    pet_held_item = pet.get("heldItem", "")
    held_item_price = LOWEST_BIN.get(pet_held_item, 0)
    pet_level_bonus = int(xp_required/10)

    #print(f"Estimated value: {base_pet_price+pet_level_bonus+held_item_price}")# made up of {base_pet_price}+{held_item_price} bonus.")
    return base_pet_price+pet_level_bonus+held_item_price
