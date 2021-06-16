from utils import human_number as hf

PRICE_SOURCE = "<:price_source:854752333299974174>"
RECOMBOBULATOR = "<:recombobulator:854750106376339477>"
ART_OF_WAR = "<:art_of_war:854750132721811466>"
HOT_POTATO_BOOK = "<:hot_potatos:854753109305065482>"
ENCHANTMENTS = "<:enchantments:854756289010728970>"
REGULAR_STARS = "<:regular_stars:854752631741480990>"
MASTER_STARS = "<:master_stars:854750116066230323>"
REFORGE = "<:reforge:854750152048246824>"

PET_ITEM = "<:minosrelic:854768366014169129>"
PET_SKIN = "<:petskin:854768054424305684>"
LEVEL = "<:level:854767687623639080>"


def do_description(value):
    elems = []
    v = value
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
    if "enchantments" in v:
        enchants_value = sum(v["enchantments"].values())
        elems.append(f"{ENCHANTMENTS} - Enchantments: +{hf(enchants_value)}")
    if "stars" in v:
        stars = v["stars"]
        elems.append(f"{REGULAR_STARS} - Regular stars: +{hf(stars['regular_stars']['total_essence_value'])}")
        if "master_stars" in stars:
            elems.append(f"{MASTER_STARS} - Master stars: +{hf(stars['master_stars'])}")
    if "reforge" in v and v["reforge"]["apply_cost"] != 0:
        reforge_item = list(v['reforge']['item'].keys())[0]
        reforge_item_cost = hf(list(v['reforge']['item'].values())[0])
        elems.append(f"{REFORGE} - Reforge ({reforge_item}) - +{reforge_item_cost}")
        
    return "\n".join(elems)

def generate_pet_description(value):
    elems = []
    v = value
    elems.append(f"{PRICE_SOURCE} - Price source: {v['price_source']}")
    if "held_item" in v:
        elems.append(f"{PET_ITEM} - Pet item: {hf(v['held_item']['value'])}")
    if "pet_skin" in v:
        elems.append(f"{PET_SKIN} - Pet skin: {hf(v['pet_skin']['value'])}")
    if "pet_level_bonus" in v:
        elems.append(f"{LEVEL} - Pet level bonus: {hf(v['pet_level_bonus']['worth'])}")
    return "\n".join(elems)
