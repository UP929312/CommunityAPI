from math import log10
import discord

async def error(ctx, title, description):
    embed = discord.Embed(title=title, description=description, colour=0xe74c3c)
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
    await ctx.send(embed=embed)

letter_values = {"": 1,
                 "k": 1000,
                 "m": 1000000,
                 "b": 1000000000}

ends = list(letter_values.keys())

def human_number(num):
    '''
    Takes an int/float e.g. 10000 and returns a formatted version e.g. 10k
    '''

    if isinstance(num, str):
        return num
    
    if num < 1: return 0

    rounded = round(num, 3 - int(log10(num)) - 1)
    suffix = ends[int(log10(rounded)/3)]
    new_num = str(rounded / letter_values[suffix])
    #new_num = new_num.remove_prefix(".0")
    return str(new_num)+suffix



