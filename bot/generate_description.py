from utils import human_number as hf

def do_description(value):
    elems = []
    v = value
    elems.append(f"<:source:854752333299974174> - Price source: {v['price_source']}")
    if "recombobulator_value" in v:
        elems.append(f"<:recombobulator:854750106376339477> - Recomobulator 5000: (+{hf(v['recombobulator_value'])})")
    if "art_of_war_value" in v:
        elems.append(f"<:art_of_war:854750132721811466> - Art of War: (+{hf(v['art_of_war_value'])})")
    if "hot_potatoes" in v:
        if "fuming_potato_books" in v['hot_potatoes']:
            potato_books = hf(v['hot_potatoes']['hot_potato_books']+v['hot_potatoes']["fuming_potato_books"])
        else:
            potato_books = hf(v['hot_potatoes']['hot_potato_books'])
        elems.append(f"<:hot_potato:854753109305065482> - Potato books: (+{potato_books})")
    if "enchantments" in v:
        enchants_value = sum(v["enchantments"].values())
        elems.append(f"<:enchanted_book:854756289010728970> - Enchantments: {hf(enchants_value)}")
    if "stars" in v:
        stars = v["stars"]
        elems.append(f"<:wither_essence:854752631741480990> - Regular stars: {hf(stars['regular_stars']['total_essence_value'])}")
        if "master_stars" in stars:
            elems.append(f"<:master_star:854750116066230323> - Master stars: {hf(stars['master_stars'])}")
    if "reforge" in v and v["reforge"]["apply_cost"] != 0:
        reforge_item = list(v['reforge']['item'].keys())[0]
        reforge_item_cost = hf(list(v['reforge']['item'].values())[0])
        elems.append(f"<:anvil:854750152048246824> - Reforge ({reforge_item}) - {reforge_item_cost}")
        
    return "\n".join(elems)


