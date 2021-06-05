from calculators.enchantment_calculator import calculate_enchantment
from calculators.pet_calculator import calculate_pet
from calculators.base_item_calculator import calculate_item

def calculate_container(elements, print_prices=False):
    total = 0
    for element in elements:            
        if isinstance(element, dict) and 'uuid' in element.keys() and 'active' in element.keys():
            price = calculate_pet(element, print_prices)
        elif element.internal_name == "ENCHANTED_BOOK":
            price = calculate_enchantment(element)
        else:
            price = calculate_item(element, print_prices)
        total += price
    return total
