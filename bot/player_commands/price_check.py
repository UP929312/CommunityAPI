import discord  # type: ignore
from discord.ext import commands  # type: ignore
from typing import Optional

import requests  # For making the api call

from utils import error, hf, find_closest
from emojis import MATHS_EMOJIS
     

class price_check_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(aliases=['price', 'p', 'pc'])
    async def price_check(self, ctx: commands.Context, *, input_item: Optional[str] = None) -> None:
        closest = await find_closest(ctx, input_item)
        if closest is None:
            return

        #print(closest)
        
        response = requests.get(f"https://sky.coflnet.com/api/item/price/{closest['internal_name']}").json()

        #print(response)

        if "Slug" in response.keys() or "min" not in response.keys():
            return await error(ctx, "Error, no items of that type could be found on the auction house!", "Try a different item instead?")

        string = [f"{MATHS_EMOJIS['min']} Minimum: {hf(response['min'])}",
                  f"{MATHS_EMOJIS['max']} Maximum: {hf(response['max'])}",
                  f"{MATHS_EMOJIS['volume']} Number sold: {hf(response['volume'])}",
                  f"{MATHS_EMOJIS['median']} Median: {hf(response['median'])}",
                  f"{MATHS_EMOJIS['mode']} Mode: {hf(response['mode'])}",
                  f"{MATHS_EMOJIS['mean']} Mean Average: {hf(response['mean'])}",
                  f"",
                  f"Links: Definitions for mode, median and mean: [link](https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/mean-median-basics/a/mean-median-and-mode-review), API: [link](https://sky.coflnet.com/data)"]
                    
        embed = discord.Embed(title=f"Price data found for {closest['name']}:", description="\n".join(string), colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)

