import discord
from math import log10
import mysql.connector

async def error(ctx, title, description):
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    await ctx.send(embed=embed)

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
    Takes an int/float e.g. 10000 and returns a formatted version e.g. 10k
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

def get_profile_data(username):
    pass


with open("database_creds.txt") as file:
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
