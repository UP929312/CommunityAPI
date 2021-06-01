import requests
import json

REFORGE = ("reforges", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/reforgestones.json", "REFORGE_DICT")
ENCHANTS = ("enchants", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/enchants.json", "ENCHANTS_DICT")
ESSENCE = ("essence", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/essencecosts.json", "ESSENCE_DICT")

for file, link, var_name in (REFORGE, ENCHANTS, ESSENCE):
    result = requests.get(link)

    with open(f"{file}.py", 'w') as file:
        string_dict = json.dumps(result.json())
        file.write(var_name+" = "+string_dict)
    print(f"Loaded in {var_name}")

#==================================================================

LOWEST_BIN = {}

request = requests.get(f"http://moulberry.codes/lowestbin.json")
if request.status_code == 200:
    data = request.json()

    for key, value in data.items():
        LOWEST_BIN[key] = value
        
    with open(f"lowest_bin.py", 'w') as file:
        file.write("LOWEST_BIN = "+json.dumps(data))

else:
    print("Error getting lowest bin data!")

print("Loaded BIN")
