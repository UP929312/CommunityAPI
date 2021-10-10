import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

import json
import requests
from difflib import SequenceMatcher

from utils import error, similar, guild_ids

initial_request = requests.get(f"https://api.hypixel.net/skyblock/bazaar").json()
ITEMS = initial_request["products"].keys()

with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    ITEM_DICT: dict = json.load(file)

items_mapped: list[tuple] = []
for item in ITEMS:
    try:
        data = (item, ITEM_DICT[item]["name"])
        items_mapped.append(data)
    except KeyError:
        pass

## The reason I don't use find-closest is because I only want to auto-correct to bazaar items, not all items

class bazaar_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="bazaar", aliases=['b', 'ba', 'baz', 'bz'])
    async def bazaar_command(self, ctx, *, input: Optional[str] = None) -> None:
        await self.bazaar(ctx, input, is_response=False)

    @commands.slash_command(name="bazaar", description="Gets bazaar data for a certain item", guild_ids=guild_ids)
    async def bazaar_slash(self, ctx, input: Option(str, "input:", required=True)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.bazaar(ctx, input, is_response=True)

    #=========================================================================================================================
    
    async def bazaar(self, ctx, user_input: Optional[str] = None, is_response: bool = False) -> None:
        if user_input is None:
            return await error(ctx, "No item given.", "Please give the item you want to check the price of at the bazaar.", is_response=is_response)

        if user_input.startswith("e "):
            user_input = "enchanted"+user_input.removeprefix("e ")
        
        closest = max(items_mapped, key=lambda _tuple: similar(_tuple[1].lower(), user_input.lower()))
        
        if similar(closest[1], user_input) < 0.5:
            return await error(ctx, "No item with that name found at the bazaar.", "Is the item availible to purchase at the bazaar?", is_response=is_response)    
            
        request = requests.get(f"https://api.hypixel.net/skyblock/bazaar").json()

        internal_name = closest[0]

        data = request["products"][internal_name]

        list_of_strings = [
            f"Buy it instantly price: ${int(data['buy_summary'][0]['pricePerUnit'])}",
            f"Sell it instantly price: ${int(data['sell_summary'][0]['pricePerUnit'])}",
            f"Buy volume: {data['quick_status']['buyVolume']}",
            f"Sell volume: {data['quick_status']['sellVolume']}",
        ]

        embed = discord.Embed(title=f"Bazaar pricing information for {closest[1]}", description="\n".join(list_of_strings), url=f"https://bazaartracker.com/product/{internal_name.lower()}", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
