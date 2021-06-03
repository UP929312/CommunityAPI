import requests
import json

#==================================================================
# CONSTANTS
ENCHANTS = ("enchants", "ENCHANTS_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/enchants.json")
ESSENCE = ("essence", "ESSENCE_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/essencecosts.json")
PETS = ("pets", "PET_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/pets.json")

for file, var_name, link in (ENCHANTS, ESSENCE, PETS):
    result = requests.get(link).json()

    with open(f"{file}.py", 'w') as file:
        file.write(f"{var_name} = "+json.dumps(result))
    print(f"Loaded in {var_name}")

#==================================================================
# REFORGE STONES
file, var_name, link = ("reforges", "REFORGE_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/reforgestones.json")
result = requests.get(link).json()
REFORGE_DICT = {}

with open(f"{file}.py", 'w') as file:
    for internal_name in result:
        reforge_name = result[internal_name]["reforgeName"].lower()
        REFORGE_DICT[reforge_name] = {"INTERNAL_NAME": internal_name,
                                       "REFORGE_COST": result[internal_name]["reforgeCosts"],}
    file.write(f"{var_name} = "+json.dumps(REFORGE_DICT))
print(f"Loaded in {var_name}")

#==================================================================
# BIN IT NOW
file, var_name, link = ("lowest_bin", "LOWEST_BIN", "http://moulberry.codes/lowestbin.json")
request = requests.get(link).json()

LOWEST_BIN = dict([(k, int(v)) for k, v in request.items()])
        
with open(f"{file}.py", 'w') as file:
    file.write(f"{var_name} = "+json.dumps(LOWEST_BIN))

print(f"Loaded in {var_name}")
#==================================================================
# BAZAAR
file, var_name, link = ("bazaar", "BAZAAR", "https://api.hypixel.net/skyblock/bazaar")
BAZAAR = {}

result = requests.get(link).json()
for product in result["products"]:
    BAZAAR[product] = int(result["products"][product]['quick_status']['sellPrice'])

with open(f"{file}.py", 'w') as file:
    file.write(f"{var_name} = "+json.dumps(BAZAAR))

