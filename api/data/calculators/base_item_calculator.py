from data.constants.reforges import REFORGE_DICT
from data.calculators.dungeon_calculator import calculate_dungeon_item
from data.calculators.enchantment_calculator import calculate_enchantments


def calculate_reforge_price(data, price):
    item = price.item
    # This "+;item.item_group prevents warped for armor and AOTE breaking
    reforge_data = REFORGE_DICT.get(item.reforge+";"+item.item_group, None)
    # This will not calculate reforges that are from the blacksmith, e.g. "Wise", "Demonic", they're just not worth anything.
    if reforge_data is not None:
        reforge_item = reforge_data["INTERNAL_NAME"]  # Gets the item, e.g. BLESSED_FRUIT
        item_rarity = item.rarity
        if item_rarity in ["SPECIAL", "VERY_SPECIAL"]:  # The dataset doesn't include special, use LEGENDARY instead
            item_rarity = "LEGENDARY"
        #print("All data:", reforge_data, "\nInternal name:", item.internal_name)
        #print(reforge_data["REFORGE_COST"], item_rarity)
        reforge_cost = reforge_data["REFORGE_COST"].get(item_rarity, 0)  # Cost to apply for each rarity

        # How much does the reforge stone cost, check bazaar
        reforge_item_cost = data.BAZAAR.get(reforge_item, 0)

        price.value["reforge"] = {}
        price.value["reforge"]["item"] = {reforge_item: reforge_item_cost}
        price.value["reforge"]["apply_cost"] = reforge_cost

    return price

def is_npc_item(data, internal_name):
    for npc, items in data.NPC_ITEMS.items():
        for item, item_price in items.items():
            if item == internal_name:
                return item_price, npc
    return None, None

def calculate_item(data, price, print_prices=False):

    item = price.item
    value = price.value

    # Calculate base price

    # If the item is in any of the npc's lists
    item_price, npc = is_npc_item(data, item.internal_name)
    if item_price is not None:
        if item.internal_name in data.LOWEST_BIN and data.LOWEST_BIN[item.internal_name] < item_price:
            value["base_price"] = data.LOWEST_BIN[item.internal_name]
            value["price_source"] = "BIN"
        else:
            value["base_price"] = item_price
            value["price_source"] = npc
    elif item.internal_name in data.BAZAAR:
        value["base_price"] = data.BAZAAR[item.internal_name]
        value["price_source"] = "Bazaar"
    elif item.internal_name in data.LOWEST_BIN:
        value["base_price"] = data.LOWEST_BIN[item.internal_name]
        value["price_source"] = "BIN"
    else:
        converted_name = item.name.upper().replace("- ", "").replace(" ", "_").replace("✪", "").replace("'", "").rstrip("_") # The Jerry price list uses the item name, not the internal_id.
        value["base_price"] = data.PRICES.get(converted_name, None)
        value["price_source"] = "Jerry"
        
        if value["base_price"] is None:
            value["base_price"] = 0
            value["price_source"] = "None"    
    #=============================================================================
    # Hoe calculations
    if item.type == "HOE" and item.hoe_material_list is not None:
        value["price_source"] = "Calculated"
        value["base_price"] = 1_000_000 + 512*data.BAZAAR[item.hoe_material_list[0]]
        if item.hoe_level >= 2:
            value["base_price"] += 256*data.BAZAAR[item.hoe_material_list[1]]
        if item.hoe_level >= 3:
            value["base_price"] += 256*data.BAZAAR[item.hoe_material_list[2]]
    # Accessories of Power
    if item.internal_name in ["POWER_TALISMAN", "POWER_RING", "POWER_ARTIFACT"]:
        value["price_source"] = "Calculated"
        value["base_price"] = 45*data.BAZAAR.get("FLAWED_RUBY_GEM", 0)  # Flawed Rubies
        if item.internal_name == "POWER_RING":
            value["base_price"] += 7*data.BAZAAR.get("FINE_RUBY_GEM", 0) + data.LOWEST_BIN.get("GEMSTONE_MIXTURE", 0)  # Fine rubies + gem mix
        if item.internal_name == "POWER_ARTIFACT":
            value["base_price"] += 33*data.LOWEST_BIN.get("GEMSTONE_MIXTURE", 0)  # More gemstone mixture
    #=============================================================================
    # Hot potato books:
    if item.hot_potatoes > 0:
        value["hot_potatoes"] = {}
        if item.hot_potatoes <= 10:
            value["hot_potatoes"]["hot_potato_books"] = item.hot_potatoes*data.BAZAAR["HOT_POTATO_BOOK"]
        else:
            value["hot_potatoes"]["hot_potato_books"] = 10*data.BAZAAR["HOT_POTATO_BOOK"]
            value["hot_potatoes"]["fuming_potato_books"] = (item.hot_potatoes-10)*data.BAZAAR["FUMING_POTATO_BOOK"]
    # Recombobulation
    if item.recombobulated and item.item_group is not None and value["price_source"] not in ["Bazaar", "None"]:
        value["recombobulator_value"] = data.BAZAAR["RECOMBOBULATOR_3000"]
    # Enchantments
    if item.enchantments:
        price = calculate_enchantments(data, price)
    # Reforge:
    if item.item_group is not None and item.reforge is not None:
        price = calculate_reforge_price(data, price)
    # Talisman enrichments
    if item.talisman_enrichment:
        value["talisman_enrichment"] = {item.talisman_enrichment: data.LOWEST_BIN.get("TALISMAN_ENRICHMENT_"+item.talisman_enrichment, 0)} 
    # Dungeon items/stars
    if item.star_upgrades:
        price = calculate_dungeon_item(data, price)
    # Art of war
    if item.art_of_war:
        value["art_of_war_value"] = data.BAZAAR["THE_ART_OF_WAR"]
    # Wood singularity
    if item.wood_singularity:
        value["wood_singularty_value"] = data.BAZAAR["WOOD_SINGULARITY"]
    # Armor skins
    if item.skin:
        value["skin"] = {}
        value["skin"][item.skin] = data.LOWEST_BIN.get(item.skin, 0)
    # Power ability scrolls: (Gemstone ability scrolls)
    if item.power_ability_scroll:
        value["power_ability_scroll"] = {}
        value["power_ability_scroll"][item.power_ability_scroll] = data.LOWEST_BIN.get(item.power_ability_scroll, 0)
    # Gems
    if item.gems:
        value["gems"] = {}
        for gem, condition in item.gems.items():
            gem_name = gem.removesuffix('_0').removesuffix('_1').removesuffix('_2').removesuffix('_3').removesuffix('_4').removesuffix('_5').removesuffix('_6')
            value["gems"][gem] = data.BAZAAR.get(f"{condition}_{gem_name}_GEM", 0)
    # Gemstone chambers
    if item.gemstone_chambers:
        value["gemstone_chambers"] = item.gemstone_chambers*data.LOWEST_BIN.get("GEMSTONE_CHAMBER", 0)
    # Farming for dummies books on hoes
    if item.farming_for_dummies:
        value["farming_for_dummies"] = item.farming_for_dummies*data.BAZAAR.get("FARMING_FOR_DUMMIES", 0)
    # Drills (upgrades)
    if item.type == "DRILL" and item.has_drill_upgrade:
        value["drill_upgrades"] = {}
        if item.drill_module_upgrade:
            value["drill_upgrades"][item.drill_module_upgrade] = data.LOWEST_BIN.get(item.drill_module_upgrade, 0)
        if item.drill_engine_upgrade:
            value["drill_upgrades"][item.drill_engine_upgrade] = data.LOWEST_BIN.get(item.drill_engine_upgrade, 0)
        if item.drill_tank_upgrade:
            value["drill_upgrades"][item.drill_tank_upgrade] = data.LOWEST_BIN.get(item.drill_tank_upgrade, 0)
    # Tuned transmission:
    if item.tuned_transmission:
        value["tuned_transmission"] = item.tuned_transmission*data.BAZAAR.get("TRANSMISSION_TUNER", 0)
    # Ethermerge
    if item.ethermerge:
        value["ethermerge"] = data.LOWEST_BIN.get("ETHERWARP_MERGER", 0)+data.LOWEST_BIN.get("ETHERWARP_CONDUIT", 0)
    # Winning bid for Midas Staff/Sword
    if item.winning_bid > 0 and item.internal_name in ["MIDAS_STAFF", "MIDAS_SWORD"]:
        value["winning_bid"] = item.winning_bid
    # Hyperion + Other scrolls (Necron's Blade Scrolls)
    if item.ability_scrolls:
        value["ability_scrolls_value"] = sum([data.BAZAAR.get(scroll, 0) for scroll in item.ability_scrolls])
    # Dyes:
    if item.dye:
        value["dye"] = {}
        value["dye"][item.dye] = data.LOWEST_BIN.get(item.dye, 0)
    #=================
        
    price.value = value
    return price
