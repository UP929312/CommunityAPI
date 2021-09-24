from data.decode_container import parse_container
from data.calculators.main_calculator_handler import calculate_container
from exceptions import InvalidProfileException, NoProfilesException, InvalidUUIDException

def get_storage(player_data):
    storage_items = []
    if not player_data.get("backpack_contents", False):
        return []
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
        
        valid_profiles = [x for x in profile_data if "last_save" in x['members'][uuid]]
        if not valid_profiles:
            raise NoProfilesException
            
        profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])

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

    # Get item groupings
    inv_contents   = parse_container(player_data.get("inv_contents", {"data": []})['data'])
    talisman_bag   = parse_container(player_data.get("talisman_bag", {"data": []})['data'])
    ender_chest    = parse_container(player_data.get("ender_chest_contents", {"data": []})['data'])
    armour         = parse_container(player_data.get("inv_armor", {"data": []})['data'])
    wardrobe       = parse_container(player_data.get("wardrobe_contents", {"data": []})['data'])
    personal_vault = parse_container(player_data.get("personal_vault_contents", {"data": []})['data'])
    storage_items  = get_storage(player_data)
    pet_items      = player_data.get("pets", [])

    return ({
            "profile_name": other_data["cute_name"],
            "profile_type": other_data.get("game_mode", "regular"),
            },
            {
            "inventory":    calculate_container(data, inv_contents),
            "accessories":  calculate_container(data, talisman_bag),
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
