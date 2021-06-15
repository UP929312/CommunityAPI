from data.networth import get_containers

async def get_groups_value(username, containers=None, extras=None):
    if containers is None and extras is None:
        containers, extras = get_containers(username)

    inventory_total   = sum(x.total for x in containers["inventory"])
    accessories_total = sum(x.total for x in containers["accessories"])
    ender_chest_total = sum(x.total for x in containers["ender_chest"])
    armour_total      = sum(x.total for x in containers["armor"])
    wardrobe_total    = sum(x.total for x in containers["wardrobe"])
    vault_total       = sum(x.total for x in containers["vault"])
    storage_total     = sum(x.total for x in containers["storage"])
    pets_total        = sum(x.total for x in containers["pets"])

    purse = extras["purse"]
    banking = extras["banking"]

    return {
            "purse":       purse,
            "banking":     banking,
            "inventory":   inventory_total,
            "accessories": accessories_total,
            "ender_chest": ender_chest_total,
            "armor":       armour_total,
            "wardrobe":    wardrobe_total,
            "vault":       vault_total,
            "storage":     storage_total,
            "pets":        pets_total
           }

