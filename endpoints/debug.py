from endpoints.groups import get_groups_value
from data.utils import human_number as hf

async def get_debug_values(username):
    containers = await get_groups_value(username)    

    # Total
    total = sum(
                [
                 containers["purse"], containers["banking"],
                 containers["inventory"], containers["accessories"],
                 containers["ender_chest"], containers["armor"],
                 containers["wardrobe"], containers["vault"],
                 containers["storage"], containers["pets"],
                ]
               )

    data = {
            "Purse": hf(containers["purse"]),
            "Bank": hf(containers["banking"]),
            "Pets": hf(containers["pets"]),
            "Inventory": hf(containers["inventory"]),
            "Accessories": hf(containers["accessories"]),
            "Ender chest": hf(containers["ender_chest"]),
            "Armor worth": hf(containers["armor"]),
            "Wardrobe": hf(containers["wardrobe"]),
            "Personal vault": hf(containers["vault"]),
            "Storage": hf(containers["storage"]),
            "Total": hf(total),
           }

    return data
