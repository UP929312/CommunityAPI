from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "XI", "X"]

def calculate_enchantment(element):
    if isinstance(element, str): # If it's a string (e.g. we're getting the enchant of an item)
        return 5
    else:  # If it's an enchanted book.
        rarity = element.description_clean[-1]
        first_line_of_desc = element.description_clean[0].split(" ")
        enchantment_type = " ".join(first_line_of_desc[:-1]).replace(" ", "_").upper()
        numeral_enchantment_level = first_line_of_desc[-1]
        
        enchantment_level = ROMAN_NUMERALS.index(numeral_enchantment_level)+1
        
        #print(f"Enchantment level: {enchantment_level}")
        #print(f"Enchantment type: {enchantment_type}")
        
        if f"{enchantment_type};{enchantment_level}" in LOWEST_BIN:
            #print("Enchanted book was found on LOWEST_BIN")
            return LOWEST_BIN[f"{enchantment_type};{enchantment_level}"]
        else:
            #print("Enchanted book will be tried on Jerry's price list")
            return PRICES.get(f"{enchantment_type.lower()}_{enchantment_level}", 0)

        
