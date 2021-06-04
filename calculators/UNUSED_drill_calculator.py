from constants.essence import ESSENCE_DICT
from constants.manual_price_checking_prices import PRICES as prices
from constants.lowest_bin import LOWEST_BIN
from constants.bazaar import BAZAAR
from constants.reforges import REFORGE_DICT

def calculate_reforge_price(item):
    # This "+;item.item_group prevents warped for armor and AOTE breaking
    reforge_data = REFORGE_DICT.get(item.reforge+";"+item.item_group, None)
    # This will not calculate reforges that are from the blacksmith, e.g. "Wise", "Demonic", they're just not worth anything.
    if reforge_data is not None:
        reforge_item = reforge_data["INTERNAL_NAME"]  # Gets the item, e.g. BLESSED_FRUIT
        item_rarity = item.rarity if item.rarity != "SPECIAL" else "LEGENDARY"  # The dataset doesn't include special, use LEGEND instead
        reforge_cost = reforge_data["REFORGE_COST"][item_rarity]  # Cost to apply for each rarity
        reforge_item_cost = LOWEST_BIN.get(f"{reforge_item}", 0)  # How much does the reforge stone cost
        
        return reforge_item_cost + reforge_cost

def calculate_item(item, print_prices=False):
    #print("BASE ITEM CALC:", item.type)
    #print(item.internal_name)
    
    if item.internal_name in BAZAAR:
        base_price = BAZAAR[item.internal_name]
    elif item.internal_name in LOWEST_BIN:
        base_price = LOWEST_BIN[item.internal_name]
    else:
        #print(f"Jerry's list: {item.internal_name}")
        base_price = prices.get(item.name.upper().replace(" ", "_"), 0)  # The price list uses the item name, not the internal_id.
        #if base_price == 0:
            #print("No price found ):")

    hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value, reforge_bonus, tali_enrichment_bonus, art_of_war_bonus, wood_singularty_bonus = (0, 0, 0, 0, 0, 0, 0, 0, 0)

    # Hot potato books:
    if item.hot_potatos > 0:
        if item.hot_potatos <= 10:
            hot_potato_value += item.hot_potatos*BAZAAR["HOT_POTATO_BOOK"]
        else:
            hot_potato_value += 10*BAZAAR["HOT_POTATO_BOOK"]+(item.hot_potatos-10)*BAZAAR["FUMING_POTATO_BOOK"]
    # Recombobulation
    if item.recombobulated:
        recombobulated_value = BAZAAR["RECOMBOBULATOR_3000"]
    # Dungeon items/stars
    if item.star_upgrades:
        star_value = calc_stars(item)
    # Enchantments
    for enchantment, level in item.enchantments.items():
        enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};{level}", 0)
    # Reforge:
    if item.item_group is not None:
        reforge_bonus = calculate_reforge_price(item)
    # Talisman enrichments
    if item.talisman_enrichment:
        tali_enrichment_bonus = LOWEST_BIN.get("TALISMAN_ENRICHMENT_"+item.talisman_enrichment, 0)
    # Art of war
    if item.art_of_war:
        art_of_war_bonus = LOWEST_BIN.get("THE_ART_OF_WAR", 0)  # Get's the art of war book from BIN
    # Wood singularty
    if item.wood_singularity:
        wood_singularty_bonus = LOWEST_BIN.get("WOOD_SINGULARITY", 0)

    # Total
    price = sum([base_price, hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value, art_of_war_bonus, wood_singularty_bonus])

    # 2 items (e.g. Enchanted Diamond Blocks) need to be worth twice as much
    price *= item.stack_size
    #=================
    if print_prices:
        print("------------")
        print(f"{item.name.upper().replace(' ', '_')} (x{item.stack_size})")
        print(f"> {price}, Recom:{recombobulated_value}, ✪: {star_value}, warped? {warped_value}, \
                enchnts: {enchants_value}, reforge: {reforge_bonus}, Art War: {art_of_war_bonus}, wood singul: {wood_singularty_bonus}\
                talisman enrichment: {tali_enrichment_bonus}")
    return price
