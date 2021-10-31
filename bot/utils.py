from math import log10
import json
import re
from difflib import SequenceMatcher
from datetime import datetime, timedelta
import discord  # type: ignore

guild_ids=[854749884103917599]
#guild_ids=None

# typing
from typing import Optional, Union

# API key for importing
with open("text_files/hypixel_api_key.txt") as file:
    API_KEY: str = file.read()

# Find closest item
with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    ITEMS: dict = json.load(file)

ENCHANT_LIST = ['bane_of_arthropods', 'cleave', 'critical', 'cubism', 'dragon_hunter', 'ender_slayer', 'execute', 'experience', 'fire_aspect', 'first_strike', 'giant_killer', 'impaling', 'knockback', 'lethality', 'life_steal', 'looting', 'luck', 'mana_steal', 'prosecute', 'scavenger', 'sharpness', 'smite', 'syphon', 'telekinesis', 'titan_killer', 'thunderlord', 'thunderbolt', 'triple_strike', 'vampirism', 'venomous', 'vicious', 'ultimate_one_for_all', 'ultimate_soul_eater', 'ultimate_chimera', 'ultimate_combo', 'ultimate_swarm', 'ultimate_wise', 'aiming', 'chance', 'flame', 'infinite_quiver', 'piercing', 'overload', 'power', 'punch', 'snipe', 'ultimate_rend', 'efficiency', 'replenish', 'silk_touch', 'turbo_cactus', 'turbo_coco', 'turbo_melon', 'turbo_pumpkin', 'delicate', 'compact', 'fortune', 'pristine', 'smelting_touch', 'angler', 'blessing', 'caster', 'expertise', 'frail', 'luck_of_the_sea', 'lure', 'magnet', 'spiked_hook', 'harvesting', 'turbo_wheat', 'turbo_cane', 'turbo_warts', 'turbo_carrot', 'turbo_potato', 'turbo_mushrooms', 'cultivating', 'big_brain', 'blast_protection', 'fire_protection', 'projectile_protection', 'protection', 'growth', 'rejuvenate', 'respite', 'aqua_affinity', 'thorns', 'respiration', 'ultimate_bank', 'ultimate_last_stand', 'ultimate_legion', 'ultimate_no_pain_no_gain', 'ultimate_wisdom', 'counter_strike', 'true_protection', 'smarty_pants', 'sugar_rush', 'feather_falling', 'depth_strider', 'frost_walker']    
PETS = ['ammonite', 'armadillo', 'baby_yeti', 'bal', 'bat', 'bee', 'black_cat', 'blaze', 'blue_whale', 'chicken', 'dolphin', 'elephant', 'ender_dragon', 'enderman', 'endermite', 'flying_fish', 'ghoul', 'giraffe', 'golden_dragon', 'golem', 'grandma_wolf', 'griffin', 'guardian', 'horse', 'hound', 'jellyfish', 'jerry', 'lion', 'magma_cube', 'megalodon', 'mithril_golem', 'monkey', 'ocelot', 'parrot', 'phoenix', 'pig', 'pigman', 'rabbit', 'rat', 'rock', 'scatha', 'sheep', 'silverfish', 'skeleton', 'skeleton_horse', 'snowman', 'spider', 'spirit', 'squid', 'tarantula', 'tiger', 'turtle', 'wither_skeleton', 'wolf', 'zombie']
PROFILE_NAMES = ['apple', 'banana', 'blueberry', 'coconut', 'cucumber', 'grapes', 'kiwi', 'lemon', 'lime', 'mango', 'orange', 'papaya', 'peach', 'pear', 'pineapple', 'pomegranate', 'raspberry', 'strawberry', 'tomato', 'watermelon', 'zucchini']
ROMAN_NUMERALS = ("x", "ix", "viii", "vii", "vi", "v", "iv", "iii", "ii", "i")

#=============================================================
# Errors
async def error(ctx, title: str, description: str, is_response: bool = False) -> None:
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    if is_response:
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.send(embed=embed)
#=============================================================

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
# returns either "item/enchant" then the dict or enchant, or None
async def smarter_find_closest(ctx, user_input: Optional[str], is_response: bool = False) -> tuple[Optional[str], Union[Optional[dict], Optional[str]]]:
    if user_input is None:
        return await error(ctx, "Error, no item given!", "This command takes the name of the item you're looking for to work!", is_response=is_response)
    #============================
    # Enchantments
    enchant_format = user_input.lower().replace(" ", "_").removesuffix("book")
    for roman_numeral in ROMAN_NUMERALS:
        if enchant_format.endswith(f"_{roman_numeral}"):
            enchant_format = enchant_format.replace(f"_{roman_numeral}", f"_{10-ROMAN_NUMERALS.index(roman_numeral)}")

    closest_enchant = max(ENCHANT_LIST, key=lambda item: similar(enchant_format, item))
    if similar(enchant_format, closest_enchant) > 0.80:
        for i in range(1, 11):
            if enchant_format.endswith(str(i)):
                return "enchant", closest_enchant+f":{i}"
        return "enchant", closest_enchant+":1"

    #============================================
    # Pets
    if "pet" in user_input.lower():
        pet_format = user_input.lower().split()
        for remove_word in ["pet", "level", "lvl", "[lvl"]:
            if remove_word in pet_format:
                pet_format.remove(remove_word)
        level, rarity = None, None
        for word in pet_format:
            if word.isdigit():
                level = word
            if word in ["common", "uncommon", "rare", "epic", "legendary", "mythic"]:
                rarity = word

        if level:
            pet_format.remove(level)
        if rarity:
            pet_format.remove(rarity)

        pet_name = "_".join(pet_format)
        closest_pet = max(PETS, key=lambda pet: similar(pet_name, pet))
        if similar(pet_name, closest_pet) > 0.80:
            return "pet", f"{closest_pet}:{rarity}:{level}"
    #=============================
    # Items    
    closest = max(ITEMS.values(), key=lambda item: similar(user_input.lower(), item["name"].lower()))
    if similar(user_input.lower(), closest["name"].lower()) > 0.6:
        return "item", closest
    #=============================
    # Nothing
    return await error(ctx, "No item, enchant or pet found with that name!", "If you're searching for a pet, please end your search with 'pet', and if you're searching for an ultimate enchantment, please include `ultimate`.", is_response=is_response) 

#=============================================================
# Formatting numbers, datetime and timedeltas
letter_values = {
    "": 1,
    "k": 1000,
    "m": 1000000,
    "b": 1000000000,
    "t": 1000000000000
}
ends = list(letter_values.keys())

def clean(string: str) -> str:
    return string.replace("_", " ").title().replace("'S", "'s")

def remove_colours(name: str) -> str:
    return re.sub('§.', '', name)

def hf(num: Union[float, str, int]) -> str:
    """
    Takes an int or float e.g. 11500 and returns a formatted version i.e. 11.5k
    """
    if isinstance(num, str):  # call float because int("5.0") will fail
        num = int(float(num))
        
    if num < 1: return "0"

    rounded = round(num, 3 - int(log10(num)) - 1)
    suffix = ends[int(log10(rounded)/3)]
    new_num = str(rounded / letter_values[suffix]).removesuffix(".0")
    return new_num+suffix

def format_duration(duration, include_millis=False):
    """
    Converts a duration in milliseconds, datetime in the future, or timedelta into a formatted duration.
    """
    if isinstance(duration, (str, int)):
        dur = timedelta(milliseconds=int(duration))
    elif isinstance(duration, datetime):
        dur = duration-datetime.now()
    else:
        dur = duration

    units = {}
    units["days"], dur = divmod(dur, timedelta(days=1))
    units["hours"], dur = divmod(dur, timedelta(hours=1))
    units["mins"], dur = divmod(dur, timedelta(minutes=1))
    units["secs"], dur = divmod(dur, timedelta(seconds=1))
    
    units["millis"] = 0 if not include_millis else int((dur / timedelta(microseconds=1)) / 1000)

    if not any(units.values()):
        return "0ms (No time given)"

    parts = []
    for timeframe, symbol in [("days", "d"), ("hours","h"),("mins","m"),("secs","s"),("millis","ms")]:
        if units[timeframe] > 0:
            parts.append(f"{units[timeframe]}{symbol}")
            
    formatted_string = ", ".join(parts)    
    return formatted_string
