from manual_price_checking_prices import PRICES as prices
from constants.lowest_bin import LOWEST_BIN

level_two_reqs = {"COMMON": 383_700, "UNCOMMON": 611_700, "RARE": 936_700, "EPIC": 1_386_700, "LEGENDARY": 1_886_700}

def calculate_pet(pet):
    # Try from LOWEST_BIN
    if f"{pet['type']};{pet['tier']}" in LOWEST_BIN:
        return LOWEST_BIN[f"{pet['type']};{pet['tier']}"]

    # Try from Jerry's list
    level_two_req = level_two_reqs[pet["tier"]]
    level = 100 if pet['exp'] >= level_two_req else 1
    price = prices.get(f"LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()}", 0)  # LVL_x_COMMON_ENDERMAN
    return price
    #print(f"Pet at LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()} priced at {price}")
