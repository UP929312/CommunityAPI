from data.container_handler import get_containers

async def get_tree(Data, username):
    containers, extras = get_containers(Data, username)

    if containers is None:
        return None

    items = ""
    for container in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
        for price_object in containers[container]:
            item = price_object.to_dump_string()
            items += item+"\n"
        
    return {"data": items}
