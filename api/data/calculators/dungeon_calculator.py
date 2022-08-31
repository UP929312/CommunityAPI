from data.constants.essence import ESSENCE_DICT

MASTER_STAR_NAMES = ['first_master_star', 'second_master_star', 'third_master_star', 'fourth_master_star', 'fifth_master_star']

#ESSENCE_ICE

def calculate_base_stars(data, price):
    item = price.item
    #print("Calc stars:", item.name, item.star_upgrades)
    essence_object = ESSENCE_DICT.get(item.internal_name.removeprefix("STARRED_"), None)
    if essence_object is None:
        #print("> CALC STARS FAILED:", item.internal_name, item.star_upgrades)
        return price
    essence_required = sum([essence_object[f"{i}"] for i in range(1, min(5, item.star_upgrades))])
    essence_type = essence_object.get("type", "Spider")   # Default to Spider, it's mid tier
    essence_type_value = data.BAZAAR.get("ESSENCE_"+essence_type.upper(), 0)   
    essence_value = essence_type_value*essence_required

    # These convert to strings so they don't get counted
    price.value["stars"]["regular_stars"] = {"essence_required": f"{essence_required}",
                                              "essence_type": f"{essence_type} ({essence_type_value} each)",
                                              "total_essence_value": essence_value}  # Needs to be an int
    return price


def calculate_dungeon_item(data, price, print_prices=False):
    item = price.item

    price.value["stars"] = {}
    price = calculate_base_stars(data, price)
    
    if item.star_upgrades > 5:
        price.value["stars"]["master_stars"] = {}
        for i in range(0, item.star_upgrades-5):
            master_star_name = MASTER_STAR_NAMES[i]
            price.value["stars"]["master_stars"][master_star_name] = data.BAZAAR.get(master_star_name.upper(), 0)

    return price

