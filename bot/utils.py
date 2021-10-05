from math import log10
import json
import re
from difflib import SequenceMatcher
from datetime import datetime, timedelta

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY: str = file.read()

ENCHANT_LIST = ['bane_of_arthropods', 'cleave', 'critical', 'cubism', 'dragon_hunter', 'ender_slayer', 'execute', 'experience', 'fire_aspect', 'first_strike', 'giant_killer', 'impaling', 'knockback', 'lethality', 'life_steal', 'looting', 'luck', 'mana_steal', 'prosecute', 'scavenger', 'sharpness', 'smite', 'syphon', 'telekinesis', 'titan_killer', 'thunderlord', 'thunderbolt', 'triple_strike', 'vampirism', 'venomous', 'vicious', 'ultimate_one_for_all', 'ultimate_soul_eater', 'ultimate_chimera', 'ultimate_combo', 'ultimate_swarm', 'ultimate_wise', 'aiming', 'chance', 'flame', 'infinite_quiver', 'piercing', 'overload', 'power', 'punch', 'snipe', 'ultimate_rend', 'efficiency', 'replenish', 'silk_touch', 'turbo_cactus', 'turbo_coco', 'turbo_melon', 'turbo_pumpkin', 'delicate', 'compact', 'fortune', 'pristine', 'smelting_touch', 'angler', 'blessing', 'caster', 'expertise', 'frail', 'luck_of_the_sea', 'lure', 'magnet', 'spiked_hook', 'harvesting', 'turbo_wheat', 'turbo_cane', 'turbo_warts', 'turbo_carrot', 'turbo_potato', 'turbo_mushrooms', 'cultivating', 'big_brain', 'blast_protection', 'fire_protection', 'projectile_protection', 'protection', 'growth', 'rejuvenate', 'respite', 'aqua_affinity', 'thorns', 'respiration', 'ultimate_bank', 'ultimate_last_stand', 'ultimate_legion', 'ultimate_no_pain_no_gain', 'ultimate_wisdom', 'counter_strike', 'true_protection', 'smarty_pants', 'sugar_rush', 'feather_falling', 'depth_strider', 'frost_walker']    
PROFILE_NAMES = ['apple', 'banana', 'blueberry', 'coconut', 'cucumber', 'grapes', 'kiwi', 'lemon', 'lime', 'mango', 'orange', 'papaya', 'peach', 'pear', 'pineapple', 'pomegranate', 'raspberry', 'strawberry', 'tomato', 'watermelon', 'zucchini']
ROMAN_NUMERALS = ("x", "ix", "viii", "vii", "vi", "v", "iv", "iii", "ii", "i")

# typing
import discord  # type: ignore
from discord.ext import commands  # type: ignore
from typing import Optional, Union

#=============================================================
# Errors and safe methods
async def error(ctx: commands.Context, title: str, description: str, is_response: bool = False) -> None:
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    if is_response:
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.send(embed=embed)

async def safe_delete(message: discord.Message) -> None:
    try:
        await message.delete()
    except (discord.errors.NotFound, discord.errors.Forbidden):
        pass

async def safe_send(user, content: str):
    try:
        await user.send(content)
    except (discord.errors.NotFound, discord.errors.Forbidden):
        pass
#=============================================================
# Find closest item
with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    ITEMS: dict = json.load(file)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    
async def find_closest(ctx: commands.Context, user_input: Optional[str]) -> Optional[dict]:
    """
    When given a rough item name, this will attempt to find the corrosponding item in the item dump (text_files/MASTER_ITEM_DICT.json)
    If it is found, it will return that item's data, else return None (after sending an error)
    """
    if user_input is None:
        return await error(ctx, "Error, no item given!", "This command takes the name of the item you're looking for to work!")

    # Convert input into internal name
    closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, user_input.lower(), item["name"].lower()).ratio())
    # Check if we found something somewhat similar:
    if SequenceMatcher(None, user_input.lower(), closest["name"].lower()).ratio() < 0.6:
        return await error(ctx, "No item found with that name!", "Try being more accurate, and exclude special characters.")

    return closest

# returns either "item/enchant" then the dict or enchant, or None
async def smarter_find_closest(ctx: commands.Context, user_input: Optional[str]) -> tuple[Optional[str], Union[Optional[dict], Optional[str]]]:
    if user_input is None:
        print("No item given?")
        return await error(ctx, "Error, no item given!", "This command takes the name of the item you're looking for to work!")
    #============================
    print("Starting enchants")
    #Enchantments
    enchant_format = user_input.lower().lstrip().rstrip().replace(" ", "_").removesuffix("book")
    for roman_numeral in ROMAN_NUMERALS:
        if enchant_format.endswith(f"_{roman_numeral}"):
            enchant_format = enchant_format.replace(f"_{roman_numeral}", f"_{10-ROMAN_NUMERALS.index(roman_numeral)}")
            
    closest_enchant = max(ENCHANT_LIST, key=lambda item: similar(enchant_format, item))
    print(closest_enchant, similar(enchant_format, closest_enchant))
    if similar(enchant_format, closest_enchant) > 0.85:
        for i in range(1, 11):
            if enchant_format.endswith(str(i)):
                return "enchant", closest_enchant+f":{i}"
        return "enchant", closest_enchant+":1"
    #=============================
    # Items    
    closest = max(ITEMS.values(), key=lambda item: similar(user_input.lower(), item["name"].lower()))
    if similar(user_input.lower(), closest["name"].lower()) > 0.6:
        return "item", closest
    #=============================
    # Nothing
    return await error(ctx, "No item, enchant or pet found with that name!", "Try being more accurate, and putting the full item name instead.")
    
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
    new_num = rounded / letter_values[suffix]
    return str(new_num)+suffix

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
