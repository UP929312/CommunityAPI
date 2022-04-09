from data.calculators.enchantment_calculator import calculate_enchanted_book
from data.calculators.pet_calculator import calculate_pet
from data.calculators.base_item_calculator import calculate_item
from data.price_object import Price

def calculate_container(data, elements, print_prices=False):    
    prices = []
    for element in elements:
        price = Price(element)

        if isinstance(element, dict) and ('candyUsed' in element.keys() or 'active' in element.keys()):
            price_object = calculate_pet(data, price, print_prices)

        elif element.internal_name == "ENCHANTED_BOOK":
            price_object = calculate_enchanted_book(data, price)

        elif element.internal_name == "PET":
            pet_info = price.item.pet_info
            element = {'uuid': None, 'type': pet_info['type'], 'exp':  pet_info['exp'], 'active': False, 'tier': pet_info["tier"],
                       'candyUsed': pet_info.get('candyUsed', 0)}
            if "skin" in pet_info:
                element['skin'] = pet_info['skin']
            if "heldItem" in pet_info:
                element['heldItem'] = pet_info['heldItem']
            price_object = calculate_pet(data, Price(element), print_prices)
        else:
            price_object = calculate_item(data, price, print_prices)

        if price_object is not None:
            price_object.calculate_total()
            prices.append(price_object)

    return prices
