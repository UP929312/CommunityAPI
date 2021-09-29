from utils import hf, clean
from networth.constants import PRICE_SOURCE, RECOMBOBULATOR, ART_OF_WAR, HOT_POTATO_BOOK, TALISMAN_ENRICHMENT, ENCHANTMENTS, REGULAR_STARS, MASTER_STARS, SKIN, POWER_ABILITY_SCROLL, GEMS, GEMSTONE_CHAMBERS, REFORGE, TRANSMISSIONS, ETHERMERGE, WINNING_BID, PET_ITEM, PET_SKIN, LEVEL

def generate_item_description(v: dict) -> str:
    elems = []
    #elems.append(f"{BASE_PRICE} - Base cost: {v['base_price']}")
    elems.append(f"{PRICE_SOURCE} - Price source: {v['price_source']}")
    if "recombobulator_value" in v:
        elems.append(f"{RECOMBOBULATOR} - Recombobulator: +{hf(v['recombobulator_value'])}")
    if "art_of_war_value" in v:
        elems.append(f"{ART_OF_WAR} - Art of War: +{hf(v['art_of_war_value'])}")
    if "hot_potatoes" in v:
        potato_books = v['hot_potatoes']['hot_potato_books']+v['hot_potatoes'].get("fuming_potato_books", 0)       
        elems.append(f"{HOT_POTATO_BOOK} - Potato books: +{hf(potato_books)}")
    if "talisman_enrichment" in v:
        enrichment_item, enrichment_value = list(v['talisman_enrichment'].items())[0]
        elems.append(f"{TALISMAN_ENRICHMENT} - Enrichment: ({clean(enrichment_item)} - {hf(enrichment_value)})")
    if "enchantments" in v:
        elems.append(f"{ENCHANTMENTS} - Enchantments: +{hf(sum(v['enchantments'].values()))}")
    if "stars" in v:  # This can sometimes be {}
        stars = v["stars"]
        if "regular_stars" in stars:
            elems.append(f"{REGULAR_STARS} - Regular stars: +{hf(stars['regular_stars']['total_essence_value'])}")
        if "master_stars" in stars:
            elems.append(f"{MASTER_STARS} - Master stars: ({len(stars['master_stars'])} stars - {hf(sum(stars['master_stars'].values()))})")
    if "skin" in v:
        skin_item, skin_value = list(v['skin'].items())[0]
        elems.append(f"{SKIN} - Skin: ({clean(skin_item)} - {hf(skin_value)})")
    if "power_ability_scroll" in v:
        power_ability_scroll_item, power_ability_scroll_value = list(v["power_ability_scroll"].items())[0]
        elems.append(f"{POWER_ABILITY_SCROLL} - Power scroll: ({clean(power_ability_scroll_item)} - {hf(power_ability_scroll_value)})") 
    if "gems" in v:
        elems.append(f"{GEMS} - Gems: {hf(sum(v['gems'].values()))}")
    if "gemstone_chambers" in v:
        elems.append(f"{GEMSTONE_CHAMBERS} - Gemstone chambers: {hf(v['gemstone_chambers'])}")
    if "reforge" in v and v["reforge"]["apply_cost"] != 0:
        reforge_item, reforge_item_cost = list(v['reforge']['item'].items())[0]
        elems.append(f"{REFORGE} - Reforge: ({clean(reforge_item)} - {reforge_item_cost})")
    if "tuned_transmission" in v:
        elems.append(f"{TRANSMISSIONS} - Tuned transmissions: {hf(v['tuned_transmission'])}")
    if "ethermerge" in v:
        elems.append(f"{ETHERMERGE} - Ethermerge: {hf(v['ethermerge'])}")
    if "winning_bid" in v:
        elems.append(f"{WINNING_BID} - Winning bid: {hf(v['winning_bid'])}")
        
    return "\n".join(elems)

def generate_pet_description(value: dict, item: dict) -> str:
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

def generate_description(value: dict, item: dict) -> str:
    if "candyUsed" in item:  # For pets only
        return generate_pet_description(value, item)
    else:
        return generate_item_description(value)
