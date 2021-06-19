from utils import hf, clean
from constants import PRICE_SOURCE, RECOMBOBULATOR, ART_OF_WAR, HOT_POTATO_BOOK, TALISMAN_ENRICHMENT, ENCHANTMENTS, REGULAR_STARS, MASTER_STARS, REFORGE, PET_ITEM, PET_SKIN, LEVEL

def generate_item_description(value, item):
    elems = []
    v = value
    #elems.append(f"{BASE_PRICE} - Base cost: {v['base_price']}")
    elems.append(f"{PRICE_SOURCE} - Price source: {v['price_source']}")
    if "recombobulator_value" in v:
        elems.append(f"{RECOMBOBULATOR} - Recomobulator: +{hf(v['recombobulator_value'])}")
    if "art_of_war_value" in v:
        elems.append(f"{ART_OF_WAR} - Art of War: +{hf(v['art_of_war_value'])}")
    if "hot_potatoes" in v:
        if "fuming_potato_books" in v['hot_potatoes']:
            potato_books = hf(v['hot_potatoes']['hot_potato_books']+v['hot_potatoes']["fuming_potato_books"])
        else:
            potato_books = hf(v['hot_potatoes']['hot_potato_books'])
        elems.append(f"{HOT_POTATO_BOOK} - Potato books: +{potato_books}")
    if "talisman_enrichment" in v:
        enrichment_item, enrichment_value = list(v['talisman_enrichment'].items())[0]
        elems.append(f"{TALISMAN_ENRICHMENT} - Enrichment: ({clean(enrichment_item)} - {hf(enrichment_value)})")
    if "enchantments" in v:
        enchants_value = sum(v["enchantments"].values())
        elems.append(f"{ENCHANTMENTS} - Enchantments: +{hf(enchants_value)}")
    if "stars" in v:
        stars = v["stars"]
        elems.append(f"{REGULAR_STARS} - Regular stars: +{hf(stars['regular_stars']['total_essence_value'])}")
        if "master_stars" in stars:
            elems.append(f"{MASTER_STARS} - Master stars: ({len(stars['master_stars'])} stars - {hf(sum(stars['master_stars'].values()))})")
    if "reforge" in v and v["reforge"]["apply_cost"] != 0:
        reforge_item = list(v['reforge']['item'].keys())[0]
        reforge_item_cost = hf(list(v['reforge']['item'].values())[0])
        elems.append(f"{REFORGE} - Reforge: ({clean(reforge_item)} - {reforge_item_cost})")
        
    return "\n".join(elems)

def generate_pet_description(value, item):
    elems = []
    v = value
    elems.append(f"{PRICE_SOURCE} - Price source: {v['price_source']}")
    if "held_item" in v:
        pet_item_formatted = item['heldItem'].removeprefix("PET_ITEM_")
        for rarity in ["_COMMON", "_UNCOMMON", "_RARE", "_EPIC", "_LEGENDARY", "_MYTHIC", "_SPECIAL", "_VERY_SPECIAL"]:
            pet_item_formatted = pet_item_formatted.removesuffix(rarity)
        elems.append(f"{PET_ITEM} - Pet item: ({clean(pet_item_formatted)} - {hf(v['held_item']['value'])})")
    if "pet_skin" in v:
        elems.append(f"{PET_SKIN} - Pet skin: ({clean(item['skin'])} - {hf(v['pet_skin']['value'])})")
    if "pet_level_bonus" in v:
        elems.append(f"{LEVEL} - Pet level bonus: {hf(v['pet_level_bonus']['worth'])}")
    return "\n".join(elems)

def generate_description(value, item):
    if "candyUsed" in item:  # For pets only
        return generate_pet_description(value, item)
    else:
        return generate_item_description(value, item)
