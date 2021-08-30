import discord
from math import log10
import json
from difflib import SequenceMatcher
from datetime import datetime, timedelta

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

#=============================================================
# Errors and safe methods
async def error(ctx, title, description):
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    await ctx.send(embed=embed)

async def safe_delete(message):
    try:
        await message.delete()
    except (discord.errors.NotFound, discord.errors.Forbidden):
        pass

async def safe_send(user, content):
    try:
        await user.send(content)
    except (discord.errors.NotFound, discord.errors.Forbidden):
        pass
#=============================================================
# Find closest item
with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    ITEMS = json.load(file)
    
async def find_closest(ctx, user_input):
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


'''
def find_closest_dev(user_input):
    closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, user_input.lower(), item["name"].lower()).ratio())
    if SequenceMatcher(None, user_input.lower(), closest["name"].lower()).ratio() < 0.6:
        print("Error")

    return closest

items = []
for item in "Aspect of the End, Aspect of the Void, Zombie Sword, Ornate Zombie Sword, Reaper Falchion, Pooch Sword, Axe of the Shredded, Yeti Sword, Midas' Sword, Daedalus Axe, Aspect of the Dragons, Bonzo's Staff, Spirit Sceptre, Adaptive Blade, Ice Spray Wand, Livid Dagger, Shadow Fury, Flower of Truth, Giant's Sword, Titanium Drill DR-X455, Titanium Drill DR-X555, Topaz Drill KGR-12, Blaze Armor, Mastiff Armor, Perfect Armor, Shark Scale Armor, Superior Dragon Armor, Adaptive Armor, Shadow Assassin Armor, Necromancer Lord Armor, Sorrow Armor.".split(","):
    items.append(find_closest_dev(item)["internal_name"])
#find_closest_dev("enchanted book")
print(items)
'''

#=============================================================
# Formatting numbers, datetime and timedeltas
letter_values = {"": 1,
                 "k": 1000,
                 "m": 1000000,
                 "b": 1000000000,
                 "t": 1000000000000}

ends = list(letter_values.keys())

def clean(string):
    return string.replace("_", " ").title().replace("'S", "'s")

def hf(num):
    """
    Takes an int or float e.g. 10000 and returns a formatted version i.e. 10k
    """
    if isinstance(num, str):
        if num.isdigit():
            num = float(num)
        else:
            return num
    
    if num < 1: return 0

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
