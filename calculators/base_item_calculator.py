from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN
from constants.bazaar import BAZAAR
from constants.reforges import REFORGE_DICT

from calculators.dungeon_calculator import calculate_dungeon_item

def calculate_reforge_price(item):
    # This "+;item.item_group prevents warped for armor and AOTE breaking
    reforge_data = REFORGE_DICT.get(item.reforge+";"+item.item_group, None)
    # This will not calculate reforges that are from the blacksmith, e.g. "Wise", "Demonic", they're just not worth anything.
    if reforge_data is not None:
        reforge_item = reforge_data["INTERNAL_NAME"]  # Gets the item, e.g. BLESSED_FRUIT
        item_rarity = item.rarity if item.rarity != "SPECIAL" else "LEGENDARY"  # The dataset doesn't include special, use LEGEND instead
        #print(reforge_data)
        #print(item.internal_name)
        #print(reforge_data["REFORGE_COST"], item_rarity)
        reforge_cost = reforge_data["REFORGE_COST"][item_rarity]  # Cost to apply for each rarity
        reforge_item_cost = LOWEST_BIN.get(f"{reforge_item}", 0)  # How much does the reforge stone cost
        
        return reforge_item_cost + reforge_cost
    return 0

def calculate_item(item, print_prices=False):

    hot_potato_value, recombobulated_value, star_value, enchants_value, reforge_bonus, tali_enrichment_bonus, art_of_war_bonus, wood_singularty_bonus, farming_for_dummies_bonus, drill_upgrades, scroll_bonus, livid_fragment_bonus = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    #print("BASE ITEM CALC:", item.type)
    #print(item.internal_name)

    converted_name = item.name.upper().replace("- ", "").replace(" ", "_") # The Jerry price list uses the item name, not the internal_id.
    
    if item.internal_name in BAZAAR:
        base_price = BAZAAR[item.internal_name]
        price_source = "Bazaar"
    elif item.internal_name in LOWEST_BIN:
        base_price = LOWEST_BIN[item.internal_name]
        price_source = "BIN"
    else:
        price_source = "Jerry"
        #print(converted_name)
        base_price = PRICES.get(converted_name, 0)  
        if base_price == 0:
            price_source = "None"

    #=============================================================================
    # Hoe calculations
    if item.mined_crops:
        base_price = 1_000_000+10**(len(f"{item.mined_crops+item.farmed_cultivating}")-2)
    #=============================================================================
    # Hot potato books:
    if item.hot_potatos > 0:
        if item.hot_potatos <= 10:
            hot_potato_value += item.hot_potatos*BAZAAR["HOT_POTATO_BOOK"]
        else:
            hot_potato_value += 10*BAZAAR["HOT_POTATO_BOOK"]+(item.hot_potatos-10)*BAZAAR["FUMING_POTATO_BOOK"]
    # Recombobulation
    if item.recombobulated:
        recombobulated_value = BAZAAR["RECOMBOBULATOR_3000"]
    # Enchantments
    for enchantment, level in item.enchantments.items():
        if f"{enchantment.upper()};{level}" in LOWEST_BIN:
            enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};{level}", 0)
        else:
            # If we can't find Sharpness 5, get 2^4 books (16), and add them together.
            enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};1", 0)*(2**(level-1))
    # Reforge:
    if item.item_group is not None:
        reforge_bonus = calculate_reforge_price(item)
    # Talisman enrichments
    if item.talisman_enrichment:
        tali_enrichment_bonus = LOWEST_BIN.get("TALISMAN_ENRICHMENT_"+item.talisman_enrichment, 0)
    # Dungeon items/stars
    if item.star_upgrades:
        star_value = calculate_dungeon_item(item)
    # Art of war
    if item.art_of_war:
        art_of_war_bonus = LOWEST_BIN.get("THE_ART_OF_WAR", 0)  # Get's the art of war book from BIN
    # Wood singularty
    if item.wood_singularity:
        wood_singularty_bonus = LOWEST_BIN.get("WOOD_SINGULARITY", 0)
    # Farming for dummies books on hoes
    if item.farming_for_dummies:
        farming_for_dummies_bonus += item.farming_for_dummies*LOWEST_BIN.get("FARMING_FOR_DUMMIES", 0)
    # Drills (upgrades)
    if item.type is not None and item.type == "drill":
        drill_upgrades = LOWEST_BIN.get(item.drill_module_upgrade, 0)
        drill_upgrades += LOWEST_BIN.get(item.drill_engine_upgrade, 0)
        drill_upgrades += LOWEST_BIN.get(item.drill_tank_upgrade, 0)
    # Hyperion scrolls
    if item.ability_scrolls:
        scroll_bonus = sum([LOWEST_BIN.get(scroll, 0) for scroll in item.ability_scrolls])
    # For Livid fragments
    if item.livid_fragments:
        livid_fragment_bonus = item.livid_fragments*LOWEST_BIN.get("LIVID_FRAGMENT", 0)
        
    # Total
    price = sum([base_price, hot_potato_value, recombobulated_value, star_value, enchants_value, art_of_war_bonus, wood_singularty_bonus, farming_for_dummies_bonus, drill_upgrades, scroll_bonus, livid_fragment_bonus])

    # 2 items (e.g. Enchanted Diamond Blocks) need to be worth twice as much
    price *= item.stack_size    
    #=================
    if print_prices and price > 100_000_000:
        print(f"{converted_name} (x{item.stack_size})")
        print("".join([f"> {int(price/1_000_000)} million, Base: {base_price}, Source: {price_source}, Recom:{recombobulated_value}, ✪: {star_value}, reforge: {reforge_bonus}\n",
              f"enchnts: {enchants_value}, Art War: {art_of_war_bonus}, wood singul: {wood_singularty_bonus}, enrichment: {tali_enrichment_bonus},\n",
              f"farming 4 Dummies: {farming_for_dummies_bonus}, drills: {drill_upgrades}, scroll bonus: {scroll_bonus}, Livid Frags: {livid_fragment_bonus}"]))
        print("--")
        print(repr(item))
        print("------------")
    return price
