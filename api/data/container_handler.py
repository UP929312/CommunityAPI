from data.decode_container import parse_container
from data.calculators.main_calculator_handler import calculate_container
from exceptions import InvalidProfileException, NoProfilesException, InvalidUUIDException

def get_storage(player_data):
    if not player_data.get("backpack_contents", False):
        return []
    storage_items = []
    for i in range(0, 19):
        page = player_data["backpack_contents"].get(str(i), {"data": []})
        storage_items.extend(parse_container(page["data"]))

    return storage_items

def get_data(profile_data, uuid, profile_name):
    uuid = uuid.replace("-", "")
    if profile_name not in ['None', 'latest', None]:
        if not (profiles := [x for x in profile_data if x["cute_name"].lower() == profile_name.lower()]):
            raise InvalidProfileException
        profile = profiles[0]
    else:
        if not any([uuid in x['members'] for x in profile_data]):
            raise InvalidUUIDException

        valid_profiles = [x for x in profile_data if uuid in x['members'] and "selected" in x]
        if not valid_profiles:
            raise NoProfilesException
        profile = max(valid_profiles, key=lambda x: x['selected'])

    if uuid not in profile['members'].keys():
        raise InvalidUUIDException

    other_data = profile
    player_data = profile["members"][uuid]
        
    return player_data, other_data


def get_containers(data, profile_data, uuid, profile_name):
    # Parse/Grab data
    player_data, other_data = get_data(profile_data, uuid, profile_name)
    
    if player_data is None:
        return None, None

    debug_items = False
    # Get item groupings
    if debug_items:
        print("Pre ALL parse containers, now testing inv_contents")
    inv_contents = parse_container(player_data.get("inv_contents", {"data": []})['data'])
    if debug_items:
        print("inv_contents parsed properly, now testing talisman_bag")
    talisman_bag = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
    if debug_items:
        print("talisman_bag parsed properly, now testing equipment")
    equipment = parse_container(player_data.get("equippment_contents", {"data": []})['data'])
    if debug_items:
        print("equipment parsed properly, now testing ender_chest")
    ender_chest = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
    if debug_items:
        print("ender_chest parsed properly, now testing armour")
    armour = parse_container(player_data.get("inv_armor", {"data": []})['data'])
    if debug_items:
        print("armour parsed properly, now testing wardrobe")
    wardrobe = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
    if debug_items:
        print("wardrobe parsed properly, now testing personal_vault")
    personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
    if debug_items:
        print("personal_vault parsed properly, now testing storage_items")
    storage_items = get_storage(player_data)
    if debug_items:
        print("storage_items parsed properly, now testing pet_items")
    pet_items = player_data.get("pets", [])
    if debug_items:
        print("pet items parsed properly, all parsing COMPLETE")

    if debug_items:
        print("Testing all `calculate_container`s")
        calculate_container(data, inv_contents)
        print("Post inv")
        calculate_container(data, talisman_bag)
        calculate_container(data, equipment)
        calculate_container(data, ender_chest)
        calculate_container(data, armour)
        calculate_container(data, wardrobe)
        calculate_container(data, personal_vault)
        calculate_container(data, storage_items)
        calculate_container(data, pet_items)
        print("All calculated properly")

    return ({
            "profile_name": other_data["cute_name"],
            "profile_type": other_data.get("game_mode", "regular"),
            },
            {
            "inventory":    calculate_container(data, inv_contents),
            "accessories":  calculate_container(data, talisman_bag),
            "equipment":    calculate_container(data, equipment),
            "ender_chest":  calculate_container(data, ender_chest),
            "armor":        calculate_container(data, armour),
            "wardrobe":     calculate_container(data, wardrobe),
            "vault":        calculate_container(data, personal_vault),
            "storage":      calculate_container(data, storage_items),
            "pets":         calculate_container(data, pet_items)
           },
           {
            "purse": int(player_data.get("coin_purse", 0)),  # For some reason, purse contains a bunch of extra decimal places.
            "banking": int(other_data.get("banking", {"balance": 0}).get("balance", 0))
           },
           )
