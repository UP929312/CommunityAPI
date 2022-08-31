from data.constants.enchants_top import ENCHANTS_TOP
from data.constants.enchantment_levels import ENCHANTMENT_LEVELS

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]

def calculate_enchanted_book(data, price):  # For enchanted books

    element = price.item

    if "Anvil" in element.description_clean[0]:
        price.value["price_source"] = "None"
        price.value["base_price"] = 0
        return price
    
    rarity = element.description_clean[-1]
    first_line_of_desc = element.description_clean[0].split(" ")
    enchantment_type = " ".join(first_line_of_desc[:-1]).replace(" ", "_").upper()
    numeral_enchantment_level = first_line_of_desc[-1]

    enchantment_level = ROMAN_NUMERALS.index(numeral_enchantment_level)+1

    if f"ENCHANTMENT_{enchantment_type}_{enchantment_level}" in data.BAZAAR:
        price.value["price_source"] = "Bazaar"
        price.value["enchantments_value"] = data.BAZAAR[f"ENCHANTMENT_{enchantment_type}_{enchantment_level}"]
        
    elif f"{enchantment_type};{enchantment_level}" in data.LOWEST_BIN:
        price.value["price_source"] = "BIN"
        price.value["enchantments_value"] = data.LOWEST_BIN[f"{enchantment_type};{enchantment_level}"]
        
    else:
        price.value["price_source"] = "Jerry"
        price.value["enchantments_value"] = data.PRICES.get(f"{enchantment_type.lower()}_{enchantment_level}", 0)

    return price

def calculate_enchantments(data, price):  # For enchantments on items

    price.value["enchantments"] = {}

    #print("Calculating item enchantments")
    for enchantment, level in price.item.enchantments.items():        
        enchant_name = enchantment.upper()

        if f"ENCHANTMENT_{enchant_name}_{level}" in data.BAZAAR:
            enchant_price = data.BAZAAR[f"ENCHANTMENT_{enchant_name}_{level}"]
            
        elif enchant_name in ["CULTIVATING", "COMPACT", "CHAMPION", "HETACOMBS", "EXPERTISE"]:
            # Special case for enchants obtained through doing tasks such as breaking crops
            enchant_price = data.LOWEST_BIN.get(f"{enchant_name};{1}", 0)

        elif f"{enchant_name};{level}" in data.LOWEST_BIN:
            enchant_price = data.LOWEST_BIN[f"{enchant_name};{level}"]
        
        else:
            #print("Couldn't find on LOWEST_BIN as level 1, or on Bazaar")
            #print(f"ENCHANTMENT_{enchant_name}_{level}")
            enchant_price = 0
            
        price.value["enchantments"][f"{enchantment}_{level}"] = enchant_price
        
    return price
