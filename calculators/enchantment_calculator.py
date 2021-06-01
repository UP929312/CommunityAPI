from manual_price_checking_prices import PRICES as prices
#from utils import LOWEST_BIN

def calculate_enchantment(element):
    if isinstance(element, str): # If it's a string (e.g. we're getting the enchant of an item)
        return 5
    else:  # If it's an enchanted book.
        rarity_type = element.description_clean[-1].split()
        print(rarity_type)
        enchantment_rarity = rarity_type[0].lower()
        enchantment_type = rarity_type[1].lower() if len(rarity_type) > 1 else None
        print(enchantment_rarity, enchantment_type)

        
