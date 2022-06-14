from data.container_handler import get_containers

async def get_tree(data, profile_data, uuid, profile_name):
    profile_data, containers, extras = get_containers(data, profile_data, uuid, profile_name)

    if containers is None:
        return None

    items = ""
    for container in ("inventory", "accessories", "equipment", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
        for price_object in containers[container]:
            item = price_object.to_dump_string()
            items += item+"\n"
        
    return {"data": items}
