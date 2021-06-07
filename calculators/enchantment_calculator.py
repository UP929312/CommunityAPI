from constants.jerry_price_list import PRICES
from constants.lowest_bin import LOWEST_BIN

from item_object import Item

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "XI", "X"]

def calculate_enchantments(element):

    if isinstance(element, Item):
        # For enchanted books
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
    else:
        # For enchantments on items
        print("Calculating item enchantments")
        if isinstance(element, dict):
            enchants_value = 0
            for enchantment, level in element.items():
                print(f"Trying level {level} {enchantment}")
                if f"{enchantment.upper()};{level}" in LOWEST_BIN:
                    print("Found on LOWEST_BIN")
                    enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};{level}", 0)
                else:
                    print("Not on LOWEST_BIN")
                    for i in range(level, 0, -1):
                        if f"{enchantment.upper()};{i}" in LOWEST_BIN:
                            break
                    else:
                        print("No enchantments of lower value")
                        return 0
                    # If we can't find Sharpness 5, we try Sharpness 4
                    print(f"Found enchantment of level {i}")
                    enchants_value += LOWEST_BIN.get(f"{enchantment.upper()};{i}", 0)*(2**(level-i))
                    print("It cost ",LOWEST_BIN.get(f'{enchantment.upper()};{i}', 0)*(2**(level-i)))
                    
            return enchants_value
        
