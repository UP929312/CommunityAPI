from calculators.enchantment_calculator import calculate_enchantment
from calculators.pet_calculator import calculate_pet
from calculators.base_item_calculator import calculate_item
from item_object import Item

def calculate_container(elements, print_prices=False):
    total = 0
    for element in elements:
        #print(element if element is not None else "Hmm")
        #if element is None:
        #    print("Here")
        #    continue
        if isinstance(element, dict) and 'uuid' in element.keys() and 'active' in element.keys():
            price = calculate_pet(element, print_prices)
        elif element.internal_name == "ENCHANTED_BOOK":
            price = calculate_enchantment(element)
        else:
            price = calculate_item(element, print_prices)
        total += price
    return total

'''
elif isinstance(element, Item) and element.internal_name is None:
            # Just ignore Pet Sitters, they break stuff.
            continue
'''
