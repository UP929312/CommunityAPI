#from essence_dict import ESSENCE_DICT, AVERAGE_REQUIRED, TYPE_DICT, ESSENCE_PRICE
#from manual_price_checking_prices import PRICES as prices
#from utils import LOWEST_BIN

LOWEST_BIN = {}
prices = {}
ESSENCE_DICT = {}
AVERAGE_REQUIRED = {}
TYPE_DICT = {}
ESSENCE_PRICE = {}

level_two_reqs = {"COMMON": 383_700, "UNCOMMON": 611_700, "RARE": 936_700, "EPIC": 1_386_700, "LEGENDARY": 1_886_700}

def calc_pets(pets):
    total = 0
    for pet in pets:
        level_two_req = level_two_reqs[pet["tier"]]
        level = 100 if pet['exp'] >= level_two_req else 1
        price = prices.get(f"LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()}", 0)  # LVL_x_COMMON_ENDERMAN
        total += price
        #print(f"Pet at LVL_{level}_{pet['tier'].upper()}_{pet['type'].upper()} priced at {price}")
        
    return total

def calc_stars(item_name, internal_id):
    '''
    #print("Calc stars:", item_name, item_name.count("✪"))        
    essence_required = ESSENCE_DICT.get(internal_id, AVERAGE_REQUIRED)[item_name.count("✪")]
    essence_type = TYPE_DICT.get(internal_id, "SPIDER")
    essence_value = ESSENCE_PRICE[essence_type]*essence_required
    #print(f"Dungeon item! Required: {essence_required}, Type: {essence_type}, Value: {essence_value}")
    return essence_value
    '''
    return 0


def calculate_items(items, print_prices=False):        
    total = 0
    
    for item in items:
        #for reforge in ("GENTLE", "ODD", "FAST", "FAIR")
        jerry_name = item.name.upper().replace(" ", "_")
        
        if item.internal_name in LOWEST_BIN:
            base_price = LOWEST_BIN[item.internal_name]
        else:
            base_price = prices.get(jerry_name, 0)  # The price list uses the item name, not the internal_id.

        hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value = (0, 0, 0, 0, 0)
    
        # Hot potato books:
        hot_potato_value += item.hot_potatos*1_000 if item.hot_potatos <= 10 else (9-item.hot_potatos)*10_000  # 9 because the previous 10 normal books equal 1 Fuming
        # Recombobulation
        if item.recombobulated:
            recombobulated_value = 5_000_000
        # Dungeon items/stars
        if "✪" in item.name:
            star_value = calc_stars(item.name, item.internal_name)
        # Warped aspect of the end
        if ('warped', 1) in item.enchantments:
            warped_value = 10_000_00 if item.rarity == "epic" else 5_000_000

        # Enchantments
        for enchantment, level in item.enchantments.items():
            if level == 6:
                enchants_value += 500_000
            elif level >= 7:
                enchants_value += 1_000_000

        price = sum([base_price, hot_potato_value, recombobulated_value, star_value, warped_value, enchants_value])

        # 2 items (e.g. Enchanted Diamond Blocks) need to be worth twice as much
        price *= item.stack_size

        # Reforges: (Coming soon?)
        #self.reforge = extras.get('modifier', None)
        #=================
        if print_prices:
            if True:#if price == 0:
                print("------------")
                print(f"{item.name.upper().replace(' ', '_')} (x{item.stack_size})")
                print(f"> {price}, Recom:{recombobulated_value}, ✪: {star_value}, warped? {warped_value}, enchnts: {enchants_value}")
        total += price
                  
    return total
