from data.container_handler import get_containers

async def get_pages_dict(data, profile_data, uuid, profile_name):
    profile_data, containers, extras = get_containers(data, profile_data, uuid, profile_name)

    if profile_data is None:
        return None

    data = {
            "profile_data": profile_data,
            "purse":        {"total": str(extras["purse"])},
            "banking":      {"total": str(extras["banking"])},
           }


    for container in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
        top_x = sorted(containers[container], key=lambda x: x.total, reverse=True)[:5]
        prices = [x.to_dict() for x in top_x]
        data[container] = {
                           "total": f"{sum(x.total for x in containers[container])}",
                           "prices": prices,
                          }

    return data
