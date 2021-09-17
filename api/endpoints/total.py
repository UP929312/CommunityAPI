from data.container_handler import get_containers

async def get_total_value(session, api_key, data, username):
    containers, extras = await get_containers(session, api_key, data, username)

    if containers is None:
        return None
    
    total = sum([x for x in extras.values()])

    for item_list in containers.values():
        total += sum(x.total for x in item_list)

    return {"total": total}
