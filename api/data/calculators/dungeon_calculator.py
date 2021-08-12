from data.constants.essence import ESSENCE_DICT

ESSENCE_PRICE = {"Wither": 4000, "Gold": 3000,
                 "Ice":    3000, "Diamond": 3000,
                 "Dragon": 1000, "Spider": 3000,
                 "Undead": 1000}

MASTER_STAR_NAMES = ['first_master_star', 'second_master_star', 'third_master_star', 'fourth_master_star']


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


def calculate_dungeon_item(Data, price, print_prices=False):
    item = price.item

    price.value["stars"] = {}
    price = calculate_base_stars(price)
    
    if item.star_upgrades > 5:
        price.value["stars"]["master_stars"] = {}
        for i in range(1, item.star_upgrades-4):
            master_star_name = MASTER_STAR_NAMES[i-1]
            price.value["stars"]["master_stars"][master_star_name] = Data.LOWEST_BIN.get(master_star_name.upper(), 0)

    return price

