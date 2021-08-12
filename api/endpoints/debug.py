from endpoints.groups import get_groups_value

async def get_debug_values(Data, username):
    containers = await get_groups_value(Data, username)

    if containers is None:
        return None

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
            "Purse": containers["purse"],
            "Bank": containers["banking"],
            "Pets": containers["pets"],
            "Inventory": containers["inventory"],
            "Accessories": containers["accessories"],
            "Ender chest": containers["ender_chest"],
            "Armor worth": containers["armor"],
            "Wardrobe": containers["wardrobe"],
            "Personal vault": containers["vault"],
            "Storage": containers["storage"],
            "Total": total,
           }

    return data
