from math import log10
import json
import re
from difflib import SequenceMatcher
from datetime import datetime, timedelta

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY: str = file.read()

enchant_list: list[str] = ['bane_of_arthropods', 'cleave', 'critical', 'cubism', 'dragon_hunter', 'ender_slayer', 'execute', 'experience', 'fire_aspect', 'first_strike', 'giant_killer', 'impaling', 'knockback', 'lethality', 'life_steal', 'looting', 'luck', 'mana_steal', 'prosecute', 'scavenger', 'sharpness', 'smite', 'syphon', 'telekinesis', 'titan_killer', 'thunderlord', 'thunderbolt', 'triple_strike', 'vampirism', 'venomous', 'vicious', 'ultimate_one_for_all', 'ultimate_soul_eater', 'ultimate_chimera', 'ultimate_combo', 'ultimate_swarm', 'ultimate_wise', 'aiming', 'chance', 'flame', 'infinite_quiver', 'piercing', 'overload', 'power', 'punch', 'snipe', 'ultimate_rend', 'efficiency', 'replenish', 'silk_touch', 'turbo_cactus', 'turbo_coco', 'turbo_melon', 'turbo_pumpkin', 'delicate', 'compact', 'fortune', 'pristine', 'smelting_touch', 'angler', 'blessing', 'caster', 'expertise', 'frail', 'luck_of_the_sea', 'lure', 'magnet', 'spiked_hook', 'harvesting', 'turbo_wheat', 'turbo_cane', 'turbo_warts', 'turbo_carrot', 'turbo_potato', 'turbo_mushrooms', 'cultivating', 'big_brain', 'blast_protection', 'fire_protection', 'projectile_protection', 'protection', 'growth', 'rejuvenate', 'respite', 'aqua_affinity', 'thorns', 'respiration', 'ultimate_bank', 'ultimate_last_stand', 'ultimate_legion', 'ultimate_no_pain_no_gain', 'ultimate_wisdom', 'counter_strike', 'true_protection', 'smarty_pants', 'sugar_rush', 'feather_falling', 'depth_strider', 'frost_walker']    

# typing
import discord  # type: ignore
from discord.ext import commands  # type: ignore
from typing import Optional, Union

#=============================================================
# Errors and safe methods
async def error(ctx: commands.Context, title: str, description: str) -> None:
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
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


# returns either "item|enchant" then the dict or enchant, or none
def find_closest_dev(user_input: str) -> tuple[Optional[str], Union[Optional[dict], Optional[str]]]:
    closest_enchant = max(enchant_list, key=lambda item: SequenceMatcher(None, user_input.lower().replace(" ", "_").removesuffix("book"), item).ratio())
    #print(SequenceMatcher(None, user_input.lower().replace(" ", "_"), closest_enchant).ratio())
    if SequenceMatcher(None, user_input.lower().replace(" ", "_").removesuffix("book"), closest_enchant).ratio() > 0.85:
        return "enchant", closest_enchant
    
    closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, user_input.lower(), item["name"].lower()).ratio())
    if SequenceMatcher(None, user_input.lower(), closest["name"].lower()).ratio() > 0.7:
        return "item", closest
    
    print("Error")
    return None, None
    

#print(find_closest_dev("dragon tracer"))

#=============================================================
# Formatting numbers, datetime and timedeltas
letter_values = {"": 1,
                       "k": 1000,
                       "m": 1000000,
                       "b": 1000000000,
                       "t": 1000000000000}

ends = list(letter_values.keys())

def clean(string: str) -> str:
    return string.replace("_", " ").title().replace("'S", "'s")

def remove_colours(name: str) -> str:
    return re.sub('§.', '', name)

def hf(num: Union[float, str, int]) -> str:
    """
    Takes an int or float e.g. 10000 and returns a formatted version i.e. 10k
    """
    if isinstance(num, str):
        if num.isdigit():
            num = float(num)
        else:
            return num  # When it's already like 2.3m
    
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
