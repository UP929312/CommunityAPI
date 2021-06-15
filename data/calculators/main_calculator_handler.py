from data.calculators.enchantment_calculator import calculate_enchanted_book
from data.calculators.pet_calculator import calculate_pet
from data.calculators.base_item_calculator import calculate_item
from data.price_object import Price

def calculate_container(elements, print_prices=False):
    prices = []
    for element in elements:

        price = Price(element)
        
        if isinstance(element, dict) and 'uuid' in element.keys() and 'active' in element.keys():
            price_object = calculate_pet(price, print_prices)
            
        elif element.internal_name == "ENCHANTED_BOOK":
            price_object = calculate_enchanted_book(price)
            
        else:
            price_object = calculate_item(price, print_prices)

        if price_object is not None:
            price_object.calculate_total()
            prices.append(price_object)

    return prices
