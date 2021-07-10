import discord
from math import log10
import mysql.connector
from string import Formatter
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
    new_num = str(rounded / letter_values[suffix])
    return str(new_num)+suffix

def format_duration(duration, include_millis=False):

    if isinstance(duration, (str, int)):
        t = timedelta(milliseconds=int(duration))
    else:
        t = duration

    dur = timedelta(milliseconds=int(duration))

    days, dur = divmod(dur, timedelta(days=1))
    hours, dur = divmod(dur, timedelta(hours=1))
    mins, dur = divmod(dur, timedelta(minutes=1))
    secs, dur = divmod(dur, timedelta(seconds=1))
    millis = int((dur / timedelta(microseconds=1)) / 1000)

    if (days, hours, mins, secs, millis) == (0, 0, 0, 0, 0):
        return "0ms (No time given)"
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")             
    if mins > 0:
        parts.append(f"{mins}m")
    if secs > 0:
        parts.append(f"{secs}s")
    if millis > 0:
        if include_millis:
            parts.append(f"{millis}ms")
        
    formatted_string = ", ".join(parts)    
    return formatted_string

def strfdelta(tdelta, fmt):
    f = Formatter()
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map( lambda x: x[1], list(f.parse(fmt)))
    rem = int(tdelta.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in l.keys():
            d[i], rem = divmod(rem, l[i])

    pre_return_string = f.format(fmt, **d)
    
    pre_return_string = pre_return_string.replace(" 0h ", " ")
    pre_return_string = pre_return_string.replace(" 0s ", " ")
    if pre_return_string.startswith("0d"):
        pre_return_string = pre_return_string.lstrip("0d ")
    if pre_return_string.endswith("0s"):
        pre_return_string = pre_return_string.rstrip(" 0s")

    return pre_return_string

#=============================================================
# Per guild prefixes

with open("text_files/database_creds.txt") as file:
    data = [x.rstrip("\n") for x in file.readlines()]

host, user, password = data

def load_guild_prefix(guild_id):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("SELECT prefix FROM guild_prefixes WHERE guild_id=%s", (guild_id,))
        records = cursor.fetchall()
        return (None if records == [] else records[0][0])
        
    except Exception as e:
        print(e)
    finally:
        cursor.close()

        
def set_guild_prefix(guild_id, prefix):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("INSERT INTO guild_prefixes (guild_id, prefix) VALUES (%s, %s)", (guild_id, prefix))
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()


def update_guild_prefix(guild_id, prefix):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("UPDATE guild_prefixes SET prefix=%s WHERE guild_id=%s", (prefix, guild_id))
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def load_prefixes():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("SELECT guild_id, prefix FROM guild_prefixes")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(e)
    finally:
        cursor.close()

#=============================================================



