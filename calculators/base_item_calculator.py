from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN
from constants.bazaar import BAZAAR
from constants.reforges import REFORGE_DICT


from calculators.dungeon_calculator import calculate_dungeon_item
from calculators.enchantment_calculator import calculate_enchantments

def calculate_reforge_price(price):
    item = price.item
    # This "+;item.item_group prevents warped for armor and AOTE breaking
    reforge_data = REFORGE_DICT.get(item.reforge+";"+item.item_group, None)
    # This will not calculate reforges that are from the blacksmith, e.g. "Wise", "Demonic", they're just not worth anything.
    if reforge_data is not None:
        reforge_item = reforge_data["INTERNAL_NAME"]  # Gets the item, e.g. BLESSED_FRUIT
        item_rarity = item.rarity
        if item_rarity in ["SPECIAL", "VERY_SPECIAL"]:  # The dataset doesn't include special, use LEGEND instead
            item_rarity = "LEGENDARY"
        #print(reforge_data)
        #print(item.internal_name)
        #print(reforge_data["REFORGE_COST"], item_rarity)
        reforge_cost = reforge_data["REFORGE_COST"][item_rarity]  # Cost to apply for each rarity
        reforge_item_cost = LOWEST_BIN.get(f"{reforge_item}", 0)  # How much does the reforge stone cost

        price.value["reforge"] = {}
        price.value["reforge"]["item"] = {reforge_item: reforge_item_cost}
        price.value["reforge"]["apply_cost"] = reforge_cost

    return price

def calculate_item(price, print_prices=False):

    item = price.item
    value = price.value

    converted_name = item.name.upper().replace("- ", "").replace(" ", "_") # The Jerry price list uses the item name, not the internal_id.
    
    if item.internal_name in BAZAAR:
        value["base_price"] = BAZAAR[item.internal_name]
        value["price_source"] = "Bazaar"
    elif item.internal_name in LOWEST_BIN:
        value["base_price"] = LOWEST_BIN[item.internal_name]
        value["price_source"] = "BIN"
    else:
        value["price_source"] = "Jerry"
        value["base_price"] = PRICES.get(converted_name, None) 
        if value["base_price"] is None:
            value["base_price"] = 0
            value["price_source"] = "None"
    #=============================================================================
    # Hoe calculations
    if item.type == "HOE" and item.hoe_material != None:
        value["base_price"] = 1_000_000+256*(BAZAAR[item.hoe_material]*(144**item.hoe_level))
        value["price_source"] = "Calculated"
    #=============================================================================
    # Hot potato books:
    if item.hot_potatos > 0:
        value["hot_potatos"] = {}
        if item.hot_potatos <= 10:
            value["hot_potatos"]["hot_potato_books"] = item.hot_potatos*BAZAAR["HOT_POTATO_BOOK"]
        else:
            value["hot_potatos"]["hot_potato_books"] = 10*BAZAAR["HOT_POTATO_BOOK"]
            value["hot_potatos"]["fuming_potato_books"] = (item.hot_potatos-10)*BAZAAR["FUMING_POTATO_BOOK"]
    # Recombobulation
    if item.recombobulated:
        value["recombobulator_value"] = BAZAAR["RECOMBOBULATOR_3000"]
    # Enchantments
    if item.enchantments:
        price = calculate_enchantments(price)
    # Reforge:
    if item.item_group is not None and item.reforge is not None:
        price = calculate_reforge_price(price)
    # Talisman enrichments
    if item.talisman_enrichment:
        value["enrichment"] = {item.talisman_enrichment: LOWEST_BIN.get("TALISMAN_ENRICHMENT_"+item.talisman_enrichment, 0)} 
    # Dungeon items/stars
    if item.star_upgrades:
        #value["star_value"] = calculate_dungeon_item(item)
        price = calculate_dungeon_item(price)
    # Art of war
    if item.art_of_war:
        value["art_of_war_value"] = LOWEST_BIN.get("THE_ART_OF_WAR", 0)  # Get's the art of war book from BIN
    # Wood singularty
    if item.wood_singularity:
        value["wood_singularty_value"] = LOWEST_BIN.get("WOOD_SINGULARITY", 0)
    # Farming for dummies books on hoes
    if item.farming_for_dummies:
        value["farming_for_dummies_bonus"] = item.farming_for_dummies*LOWEST_BIN.get("FARMING_FOR_DUMMIES", 0)
    # Drills (upgrades)
    if item.type == "DRILL" and item.has_drill_upgrade:
        value["drill_upgrades"] = {}
        if item.drill_module_upgrade:
            value["drill_upgrades"][item.drill_module_upgrade] = LOWEST_BIN.get(item.drill_module_upgrade, 0)
        if item.drill_engine_upgrade:
            value["drill_upgrades"][item.drill_engine_upgrade] = LOWEST_BIN.get(item.drill_engine_upgrade, 0)
        if item.drill_tank_upgrade:
            value["drill_upgrades"][item.drill_tank_upgrade] = LOWEST_BIN.get(item.drill_tank_upgrade, 0)
    # Hyperion scrolls
    if item.ability_scrolls:
        value["ability_scrolls_value"] = sum([LOWEST_BIN.get(scroll, 0) for scroll in item.ability_scrolls])
    # For Livid fragments
    #if item.livid_fragments:
    #    value["livid_fragment_value"] = item.livid_fragments*LOWEST_BIN.get("LIVID_FRAGMENT", 0)
    #=================
    price.value = value
    return price
