import discord
from math import log10
from datetime import datetime, timedelta

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
    '''
    Takes an int/float e.g. 10000 and returns a formatted version i.e. 10k
    '''
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

    if isinstance(duration, (str, int)):
        dur = timedelta(milliseconds=int(duration))
    else:
        dur = duration

    units = {}
    units["days"], dur = divmod(dur, timedelta(days=1))
    units["hours"], dur = divmod(dur, timedelta(hours=1))
    units["mins"], dur = divmod(dur, timedelta(minutes=1))
    units["secs"], dur = divmod(dur, timedelta(seconds=1))
    
    units["millis"] = 0 if not include_millis else int((dur / timedelta(microseconds=1)) / 1000)

    if not any([v for v in units.values()]):
        return "0ms (No time given)"

    parts = []
    for timeframe, symbol in [("days", "d"), ("hours","h"),("mins","m"),("secs","s"),("millis","ms")]:
        if units[timeframe] > 0:
            parts.append(f"{units[timeframe]}{symbol}")
            
    formatted_string = ", ".join(parts)    
    return formatted_string
