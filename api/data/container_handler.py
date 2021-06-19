from data.decode_container import parse_container
from data.calculators.main_calculator_handler import calculate_container
from data.utils import get_data, get_storage


def get_containers(username):
    # Parse/Grab data
    player_data, other_data = get_data(username)

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
            "inventory":     calculate_container(inv_contents),
            "accessories":   calculate_container(talisman_bag),
            "ender_chest":   calculate_container(ender_chest),
            "armor":         calculate_container(armour),
            "wardrobe":      calculate_container(wardrobe),
            "vault":         calculate_container(personal_vault),
            "storage":       calculate_container(storage_items),
            "pets":          calculate_container(pet_items)
           },
           {
            "purse": int(player_data.get("coin_purse", 0)),  # For some reason, purse contains a bunch of extra decimal places.
            "banking": int(other_data.get("banking", {"balance": 0}).get("balance", 0))
           },
           )
