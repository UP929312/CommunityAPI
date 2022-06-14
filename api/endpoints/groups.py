from data.container_handler import get_containers

async def get_groups_value(data, profile_data, uuid, profile_name):
    profile_data, containers, extras = get_containers(data, profile_data, uuid, profile_name)

    if profile_data is None:
        return None

    inventory_total   = sum(x.total for x in containers["inventory"])
    accessories_total = sum(x.total for x in containers["accessories"])
    equipment_total   = sum(x.total for x in containers["equippment_contents"])
    ender_chest_total = sum(x.total for x in containers["ender_chest"])
    armour_total      = sum(x.total for x in containers["armor"])
    wardrobe_total    = sum(x.total for x in containers["wardrobe"])
    vault_total       = sum(x.total for x in containers["vault"])
    storage_total     = sum(x.total for x in containers["storage"])
    pets_total        = sum(x.total for x in containers["pets"])

    purse = extras["purse"]
    banking = extras["banking"]

    return {
            "profile_data": profile_data,
            "purse":        purse,
            "banking":      banking,
            "inventory":    inventory_total,
            "accessories":  accessories_total,
            "equipment":    equipment_total,
            "ender_chest":  ender_chest_total,
            "armor":        armour_total,
            "wardrobe":     wardrobe_total,
            "vault":        vault_total,
            "storage":      storage_total,
            "pets":         pets_total
           }

