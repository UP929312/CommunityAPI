import discord
from discord.ext import commands

import requests

from extract_ids import extract_nbt_dicts
from utils import error, hf

class lowest_bin_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['lb', 'bin'])
    async def lowest_bin(self, ctx, *, input_item=None):
        query = '{"item_name":"'+input_item+'"}'
        response = requests.get('https://api.eastarcti.ca/auctions/?query='+query).json()
        prices = [item for item in response if item.get('bin', False)]
        
        if not prices:
            return await error(ctx, "Error, not item found with that name!", "Try inputting the internal id of the item instead?")

        price = min(prices, key=lambda item: item['starting_bid'])
        item_data = extract_nbt_dicts(price['item_bytes'])
        #print(item_data)

        embed = discord.Embed(title=f"Lowest bin found for {price['item_name']}", description=f"Starting bid: {hf(price['starting_bid'])}", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
