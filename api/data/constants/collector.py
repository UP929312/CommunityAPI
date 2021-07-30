import requests
import json

def fetch_constants():
    #==================================================================
    # CONSTANTS
    ENCHANTS = ("enchants", "ENCHANTS_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/enchants.json")
    ESSENCE = ("essence", "ESSENCE_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/essencecosts.json")

    for file, var_name, link in (ENCHANTS, ESSENCE):
        result = requests.get(link).json()

        with open(f"{file}.py", 'w') as file:
            file.write(f"{var_name} = "+json.dumps(result, indent=4))
        print(f"Loaded in {var_name}")

    #==================================================================
    # REFORGE STONES
    file, var_name, link = ("pets", "PET_LEVELS", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/pets.json")
    result = requests.get(link).json()

    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(result['pet_levels'], indent=4))
    print(f"Loaded in {var_name}")

    #==================================================================
    # REFORGE STONES
    file, var_name, link = ("reforges", "REFORGE_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/reforgestones.json")
    result = requests.get(link).json()
    REFORGE_DICT = {}

    with open(f"{file}.py", 'w') as file:
        for internal_name in result:
            reforge_name = result[internal_name]["reforgeName"].lower()
            item_type = result[internal_name]["itemTypes"]
            if "/" in item_type:
                item_list = item_type.split("/")
            elif item_type == "ARMOR":
                item_list = ("HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS")
            else:
                item_list = (item_type, )
                
            for item in item_list:
                REFORGE_DICT[reforge_name+";"+item] = {"INTERNAL_NAME": internal_name,
                                               "REFORGE_COST": result[internal_name]["reforgeCosts"],}
        file.write(f"{var_name} = "+json.dumps(REFORGE_DICT, indent=4))
    print(f"Loaded in {var_name}")
    #==================================================================
    # BUY IT NOW
    file, var_name, link = ("lowest_bin", "LOWEST_BIN", "http://moulberry.codes/lowestbin.json")
    request = requests.get(link).json()

    LOWEST_BIN = dict([(k, int(v)) for k, v in request.items()])
            
    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(LOWEST_BIN, indent=4))

    print(f"Loaded in {var_name}")
    #==================================================================
    # ENCHANTS TOP NORMALLY ACHIEVABLE LEVEL
    file, var_name, link = ("enchants_top", "ENCHANTS_TOP", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/enchants.json")
    result = requests.get(link).json()

    ENCHANTS_TOP = result["enchants_min_level"]

    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(ENCHANTS_TOP, indent=4))

    print(f"Loaded in {var_name}")
    #=========================
    # Enchants that can be got at the enchanting table (not bin anymore)
    file, var_name = ("enchantment_levels", "ENCHANTMENT_LEVELS")
    ENCHANTS_LEVELS = result["enchants_xp_cost"]

    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(ENCHANTS_LEVELS, indent=4))

    print(f"Loaded in {var_name}")
    #==================================================================
    # BAZAAR
    file, var_name, link = ("bazaar", "BAZAAR", "https://api.hypixel.net/skyblock/bazaar")
    BAZAAR = {}

    result = requests.get(link).json()
    for product in result["products"]:
        BAZAAR[product] = int(result["products"][product]['quick_status']['buyPrice'])

    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(BAZAAR, indent=4))

    #==================================================================
    # JERRY'S PRICE LIST
    file, var_name, link = ("jerry_price_list", "PRICES", "https://raw.githubusercontent.com/skyblockz/pricecheckbot/master/data.json")
    PRICES = {}

    result = requests.get(link).json()
    for item in result:
        name = item["name"].upper()
        price = int((item["low"]+item["hi"])/2)
        PRICES[name] = price
        
    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(PRICES, indent=4))

    print(f"Loaded in {var_name}")

if __name__ == "__main__":
    fetch_constants()
