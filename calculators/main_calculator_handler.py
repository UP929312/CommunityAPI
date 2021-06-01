from calculators.enchantment_calculator import calculate_enchantment
from calculators.pet_calculator import calculate_pet
from calculators.base_item_calculator import calculate_item


def calculate_container(elements, print_prices=False):

    total = 0
    for element in elements:
        #if not isinstance(element, dict):
        #    print(element.internal_name)
            
        if isinstance(element, dict) and 'uuid' in element.keys() and 'active' in element.keys():
            price = calculate_pet(element)
        elif element.internal_name == "ENCHANTED_BOOK":
            print(element.internal_name)
            price = calculate_enchanted_book(element)
        else:
            price = calculate_item(element, print_prices=False)
        total += price
    return total
