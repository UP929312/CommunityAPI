import requests
import json

# REFORGE STONES
file, var_name, link = ("reforges", "REFORGE_DICT", "https://raw.githubusercontent.com/Moulberry/NotEnoughUpdates-REPO/master/constants/reforgestones.json")
result = requests.get(link).json()
REFORGE_DICT = {}

with open(f"{file}.py", 'w') as file:
    for internal_name in result:
        reforge_name = result[internal_name]["reforgeName"].lower()
        item_type = result[internal_name]["itemTypes"]
        if "/" in item_type:
            for item in item_type.split("/"):
                REFORGE_DICT[reforge_name+";"+item] = {"INTERNAL_NAME": internal_name,
                                                       "REFORGE_COST": result[internal_name]["reforgeCosts"],}
        elif item_type == "ARMOR":
            for item in ["HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS"]:
                REFORGE_DICT[reforge_name+";"+item] = {"INTERNAL_NAME": internal_name,
                                                       "REFORGE_COST": result[internal_name]["reforgeCosts"],}
        else:
            REFORGE_DICT[reforge_name+";"+item_type] = {"INTERNAL_NAME": internal_name,
                                                        "REFORGE_COST": result[internal_name]["reforgeCosts"],}
    file.write(f"{var_name} = "+json.dumps(REFORGE_DICT))
print(f"Loaded in {var_name}")
