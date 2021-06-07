from constants.essence import ESSENCE_DICT
from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN

ESSENCE_PRICE = {"Wither": 4000, "Gold": 3000,
                 "Ice": 3000,    "Diamond": 3000,
                 "Dragon": 1000, "Spider": 3000,
                 "Undead": 2000}

MASTER_STARS = {1: LOWEST_BIN["FIRST_MASTER_STAR"],
                2: LOWEST_BIN["SECOND_MASTER_STAR"],
                3: LOWEST_BIN["THIRD_MASTER_STAR"],
                4: LOWEST_BIN["FOURTH_MASTER_STAR"]}

def calc_stars(item):
    #print("Calc stars:", item.name, item.star_upgrades)
    essence_object = ESSENCE_DICT.get(item.internal_name.removeprefix("STARRED_"), None)
    if essence_object is None:
        print("> CALC STARS FAILED:", item.internal_name, item.star_upgrades)
        return 0
    essence_required = sum([essence_object[f"{i}"] for i in range(1, min(5, item.star_upgrades))])
    essence_type = essence_object.get("type", "Spider")   # Default to Spider, it's mid tier
    essence_value = ESSENCE_PRICE[essence_type]*essence_required
    #print(f"Dungeon item! Required: {essence_required}, Type: {essence_type}, Value: {essence_value}")
    return essence_value


def calculate_dungeon_item(item, print_prices=False):
    base_star_value = calc_stars(item)
    master_star_value = 0
    if item.star_upgrades > 5:
        for i in range(1, item.star_upgrades-4):
            master_star_value += MASTER_STARS[i]
    #print(f"The item's {item.star_upgrades} stars are worth {base_star_value}, with master stars being worth {master_star_value}")
    return base_star_value+master_star_value
