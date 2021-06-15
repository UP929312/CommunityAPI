from data.constants.essence import ESSENCE_DICT
from data.constants.lowest_bin import LOWEST_BIN

ESSENCE_PRICE = {"Wither": 4000, "Gold": 3000,
                 "Ice":    3000, "Diamond": 3000,
                 "Dragon": 1000, "Spider": 3000,
                 "Undead": 1000}

MASTER_STAR_NAMES = ["FIRST_MASTER_STAR", "SECOND_MASTER_STAR", "THIRD_MASTER_STAR", "FOURTH_MASTER_STAR"]

MASTER_STARS = {1: LOWEST_BIN["FIRST_MASTER_STAR"],
                2: LOWEST_BIN["SECOND_MASTER_STAR"],
                3: LOWEST_BIN["THIRD_MASTER_STAR"],
                4: LOWEST_BIN["FOURTH_MASTER_STAR"]}

def calculate_base_stars(price):
    item = price.item
    #print("Calc stars:", item.name, item.star_upgrades)
    essence_object = ESSENCE_DICT.get(item.internal_name.removeprefix("STARRED_"), None)
    if essence_object is None:
        #print("> CALC STARS FAILED:", item.internal_name, item.star_upgrades)
        return price
    essence_required = sum([essence_object[f"{i}"] for i in range(1, min(5, item.star_upgrades))])
    essence_type = essence_object.get("type", "Spider")   # Default to Spider, it's mid tier
    essence_type_value = ESSENCE_PRICE[essence_type]
    essence_value = essence_type_value*essence_required

    # These convert to strings so they don't get counted
    price.value["stars"]["regular_stars"] = {"essence_required": f"{essence_required}",
                                              "essence_type": f"{essence_type} ({essence_type_value} each)",
                                              "total_essence_value": essence_value}  # Needs to be an int
    return price


def calculate_dungeon_item(price, print_prices=False):
    item = price.item

    price.value["stars"] = {}
    price = calculate_base_stars(price)
    
    if item.star_upgrades > 5:
        price.value["stars"]["master_stars"] = 0
        for i in range(1, item.star_upgrades-4):
            price.value["stars"]["master_stars"] += MASTER_STARS[i]

    return price

