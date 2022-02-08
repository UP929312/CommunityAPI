from data.constants.pets import PET_LEVELS
PET_LEVELS = PET_LEVELS+[50000000000000000000]

RARITY_OFFSET = {"COMMON": 0, "UNCOMMON": 6, "RARE": 11, "EPIC": 16, "LEGENDARY": 20, "MYTHIC": 20}
TIERS = list(RARITY_OFFSET.keys())

COINS_PER_XP = 0.2
COINS_PER_XP_TWO_HUNDRED = 3
PET_LEVELS_SUMMED = sum(PET_LEVELS[RARITY_OFFSET["LEGENDARY"]:-1])

def get_pet_level(pet):
    pet_xp = pet["exp"]
    xp_offset = RARITY_OFFSET[pet["tier"]]
    
    pet_level = 1  
    while pet_xp > 0 and pet_level < 100:
        pet_xp -= PET_LEVELS[pet_level+xp_offset]
        pet_level += 1

    return pet_level    
    
def calculate_pet(data, price, print_prices):

    pet = price.item
    value = price.value

    # These can't be sold, so ignore their pet xp value and items
    if pet['type'] == "GRANDMA_WOLF":
        price.value = value
        return price        

    if pet['type'] == "GOLDEN_DRAGON" and pet['exp'] > PET_LEVELS_SUMMED:
        # Dragon required 1.8m xp for each level 103-200,
        # 101 is insta recieved on hatching and 102 is weirdly broken...
        pet_level = min(100+int((pet["exp"]-PET_LEVELS_SUMMED)//1_886_700)+2, 200) 
    else:    
        pet_level = get_pet_level(pet)

    #######################################################################################
    # BASE VALUE
    if f"{pet['type']};{TIERS.index(pet['tier'])}" in data.LOWEST_BIN:
        # Try from LOWEST_BIN
        value["base_price"] = data.LOWEST_BIN[f"{pet['type']};{TIERS.index(pet['tier'])}"]
        value["price_source"] = "BIN"
    else:
        # Try from Jerry's list
        value["base_price"] = data.PRICES.get(f"LVL_1_{pet['tier']}_{pet['type']}", 0)  # LVL_1_COMMON_ENDERMAN
        value["price_source"] = "Jerry"

    #######################################################################################
    # PET ITEM VALUE
    pet_held_item = pet.get("heldItem", "")
    if pet_held_item:
        value["held_item"] = {}
        value["held_item"]["item"] = pet_held_item
        value["held_item"]["value"] = data.LOWEST_BIN.get(pet_held_item, 0)
        value["held_item"]["price_source"] = "BIN"
        
    #######################################################################################
    # PET SKIN VALUE
    pet_skin = pet.get("skin", False)
    if pet_skin:
        value["pet_skin"] = {}
        value["pet_skin"]["item"] = "PET_SKIN_"+pet['skin']
        value["pet_skin"]["value"] = data.LOWEST_BIN.get("PET_SKIN_"+pet['skin'], 0)
        value["pet_skin"]["price_source"] = "BIN"

    #######################################################################################
    # PET LEVEL BONUS
    value["pet_level_bonus"] = {}
    value["pet_level_bonus"]["amount"] = f"{int(pet['exp'])} xp"
    value["pet_level_bonus"]["price_source"] = "Calculated"

    if pet_level >= 100:
        offset = RARITY_OFFSET[pet["tier"]]-1
        level_100_amount = sum(PET_LEVELS[offset:100+offset])
        pet_xp_capped = min(pet["exp"], level_100_amount)
    else:
        pet_xp_capped = pet["exp"]

    value["pet_level_bonus"]["worth"] = int(pet_xp_capped*COINS_PER_XP)  # 5 Xp = 1 coin, seems about right but this is subjective.

    if pet_level > 100:  # If it's level is over 100, i.e. it's a Golden Dragon, give each level's worth of xp a 3x multiplier
        value["pet_level_bonus"]["worth"] += (pet_level-100)*1_886_700*COINS_PER_XP_TWO_HUNDRED

    #######################################################################################
    value["pet_level"] = f"{pet_level}"

    price.value = value
    return price
