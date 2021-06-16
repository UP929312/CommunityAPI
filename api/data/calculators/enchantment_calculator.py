from data.constants.jerry_price_list import PRICES
from data.constants.lowest_bin import LOWEST_BIN

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "XI", "X"]

def calculate_enchanted_book(price):  # For enchanted books

    element = price.item
    
    rarity = element.description_clean[-1]
    first_line_of_desc = element.description_clean[0].split(" ")
    enchantment_type = " ".join(first_line_of_desc[:-1]).replace(" ", "_").upper()
    numeral_enchantment_level = first_line_of_desc[-1]
    
    enchantment_level = ROMAN_NUMERALS.index(numeral_enchantment_level)+1
    
    if f"{enchantment_type};{enchantment_level}" in LOWEST_BIN:
        #print("Enchanted book was found on LOWEST_BIN")
        price.value["price_source"] = "BIN"
        price.value["enchantments_value"] = LOWEST_BIN[f"{enchantment_type};{enchantment_level}"]
    else:
        #print("Enchanted book will be tried on Jerry's price list")
        price.value["price_source"] = "Jerry"
        price.value["enchantments_value"] = PRICES.get(f"{enchantment_type.lower()}_{enchantment_level}", 0)

    return price

def calculate_enchantments(price):  # For enchantments on items

    price.value["enchantments"] = {}

    #print("Calculating item enchantments")
    for enchantment, level in price.item.enchantments.items():
        for i in range(level, 0, -1):
            if f"{enchantment.upper()};{i}" in LOWEST_BIN:
                break
        else:
            continue  # No break, when we can't find any of that enchantment whatsoever.
        # If we can't find Sharpness 5, we try Sharpness 4
        # If the starting level is level 4, and we've found a level 2 book, we need 2**2 (4-2) books
        price.value["enchantments"][enchantment+f"_{level}"] = LOWEST_BIN.get(f"{enchantment.upper()};{i}", 0)*(2**(level-i))
    return price       
