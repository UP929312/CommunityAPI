import discord
from discord.ext import commands

import requests  # For making the api call

from utils import error, hf, RARITY_DICT, find_closest

EMOJIS = {
    "min": "<:minimum:870299134454812672>",
    "max": "<:maximum:870299134349967420>",
    "volume": "<:volume:870301300083003423>",
    "median": "<:median:870304273429327903>",
    "mode": "<:mode:870304273806802955>",
    "mean": "<:mean:870299134467407902>",  
}
     

class price_check_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['price', 'p', 'pc'])
    async def price_check(self, ctx, *, input_item=None):
        closest = await find_closest(ctx, input_item)
        if closest is None:
            return
        
        response = requests.get(f"https://sky-preview.coflnet.com/api/item/price/{closest['internal_name']}").json()

        if "Slug" in response.keys() or "min" not in response.keys():
            return await error(ctx, "Error, not items of that type could be found on the auction house!", "Try a different item instead?")

        string = [f"{EMOJIS['min']} Minimum: {hf(response['min'])}",
                  f"{EMOJIS['max']} Maximum: {hf(response['max'])}",
                  f"{EMOJIS['volume']} Number sold: {hf(response['volume'])}",
                  f"{EMOJIS['median']} Median: {hf(response['median'])}",
                  f"{EMOJIS['mode']} Mode: {hf(response['mode'])}",
                  f"{EMOJIS['mean']} Mean Average: {hf(response['mean'])}",
                  f"",
                  f"Links: Definitions for mode, median and mean: [link](https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/mean-median-basics/a/mean-median-and-mode-review), API: [link](https://sky.coflnet.com)"]
                    
        embed = discord.Embed(title=f"Price data found for {closest['name']}:", description="\n".join(string), colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)

