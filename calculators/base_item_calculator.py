from constants.essence import ESSENCE_DICT
from constants.manual_price_checking_prices import PRICES as prices
from constants.lowest_bin import LOWEST_BIN
from constants.bazaar import BAZAAR

ESSENCE_PRICE = {"Wither": 5000, "Gold": 3000,
                 "Ice": 3000,    "Diamond": 3000,
                 "Dragon": 1000, "Spider": 3000,
                 "Undead": 2000}

def calc_stars(item_name, internal_id):
    #print("Calc stars:", item_name, item_name.count("✪"))
    essence_object = ESSENCE_DICT.get(internal_id.removeprefix("STARRED_"), None)
    if essence_object is None:
        print("CALC STARS FAILED:", internal_id, item_name)
        return 0
    essence_required = sum([essence_object[f"{i}"] for i in range(1, item_name.count("✪"))])
    essence_value = ESSENCE_PRICE[essence_object.get("type", "Spider")]*essence_required
    #print(f"Dungeon item! Required: {essence_required}, Type: {essence_type}, Value: {essence_value}")
    return essence_value

def calculate_item(item, print_prices=False):        
    if item.internal_name in BAZAAR:
        base_price = int(BAZAAR[item.internal_name])
    if item.internal_name in LOWEST_BIN:
        base_price = int(LOWEST_BIN[item.internal_name])
    else:
        base_price = prices.get(item.name.upper().replace(" ", "_"), 0)  # The price list uses the item name, not the internal_id.

    hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value = (0, 0, 0, 0, 0)

    # Hot potato books:
    if item.hot_potatos > 0:
        if item.hot_potatos <= 10:
            hot_potato_value += item.hot_potatos*BAZAAR["HOT_POTATO_BOOK"]
        else:
            hot_potato_value += 10*BAZAAR["HOT_POTATO_BOOK"]+(10-item.hot_potatos)*BAZAAR["FUMING_POTATO_BOOK"]
     # Recombobulation
    if item.recombobulated:
        recombobulated_value = int(BAZAAR["RECOMBOBULATOR_3000"])
    # Dungeon items/stars
    if "✪" in item.name:
        star_value = calc_stars(item.name, item.internal_name)
    # Warped aspect of the end
    if ('warped', 1) in item.enchantments:
        warped_stone_price = LOWEST_BIN.get("AOTE_STONE", 5_000_000)
        warped_value = warped_stone_price+10_000_000 if item.rarity == "epic" else warped_stone_price+5_000_000

    # Enchantments
    for enchantment, level in item.enchantments.items():
        enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};{level}", 0)

    price = sum([base_price, hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value])

    # 2 items (e.g. Enchanted Diamond Blocks) need to be worth twice as much
    price *= item.stack_size

    # Reforges: (Coming soon?)
    #self.reforge = extras.get('modifier', None)
    #=================
    if print_prices:
        print("------------")
        print(f"{item.name.upper().replace(' ', '_')} (x{item.stack_size})")
        print(f"> {price}, Recom:{recombobulated_value}, ✪: {star_value}, warped? {warped_value}, enchnts: {enchants_value}")
    return price
