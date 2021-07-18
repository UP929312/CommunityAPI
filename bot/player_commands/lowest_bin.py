import discord
from discord.ext import commands

from difflib import SequenceMatcher

import requests
import json

from extract_ids import extract_nbt_dicts, extract_internal_names
from utils import error, hf

with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    ITEMS = json.load(file)

class lowest_bin_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['lb', 'bin'])
    async def lowest_bin(self, ctx, *, input_item=None):
        if input_item is None:
            return await error(ctx, "Error, no item given!", "This command takes the name of the item you're looking for to work!")

        # Convert input into internal name
        closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, input_item.lower(), item["name"].lower()).ratio())

        #print("Closest=", closest)

        # Check if we found something somewhat similar:
        if SequenceMatcher(None, input_item.lower(), closest["name"].lower()).ratio() < 0.6:
            return await error(ctx, "No item found with that name!", "Try being more accurate, and exclude special characters.")

        internal_name = closest["internal_name"]

        #print("Internal_name:", internal_name)

        response = requests.get('https://api.eastarcti.ca/auctions/?query={"bin":true}').json()
        #print("Response recieved")

        #print(response[0])

        items_of_type = [item for item in response if extract_internal_names(item["item_bytes"])[0] == internal_name.upper()]

        #print("Items of same type:", len(items_of_type))

        if not items_of_type:
            return await error(ctx, "Error, not items of that type could be found on the auction house!", "Try a different item instead?")

        cheapest_item = min(items_of_type, key=lambda item: item["starting_bid"])

        #print("Cheapest=", cheapest_item)
          
        item_data = extract_nbt_dicts(cheapest_item['item_bytes'])
        #print(item_data)

        embed = discord.Embed(title=f"Lowest bin found for {cheapest_item['item_name']}", description=f"Starting bid: {hf(cheapest_item['starting_bid'])}", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
