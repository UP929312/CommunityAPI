import json

from endpoints.groups import get_groups_value
from data.container_handler import get_containers

async def get_pages_dict(Data, username):
    containers, extras = get_containers(Data, username)

    if containers is None:
        return None
    
    container_values = await get_groups_value(Data, username, containers, extras)

    data = {"purse":   {"total": str(container_values["purse"])},
            "banking": {"total": str(container_values["banking"])},
           }

    for container in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
        top_x = sorted(containers[container], key=lambda x: x.total, reverse=True)[:5]
        prices = [x.to_dict() for x in top_x]
        data[container] = {
                           "total": str(container_values[container]),
                           "prices": prices,
                          }

    return data
