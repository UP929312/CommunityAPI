import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests  # For making the api call

from utils import error, hf, smarter_find_closest, bot_can_send, guild_ids
from emojis import MATHS_EMOJIS
     

class price_check_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot


    @commands.command(name="price_check", aliases=['price', 'p', 'pc'])
    async def price_check_command(self, ctx, *, input: Optional[str] = None) -> None:
        await self.price_check(ctx, input, is_response=False)

    @commands.slash_command(name="price_check", description="Gets the historic price data about an item", guild_ids=guild_ids)
    async def price_check_slash(self, ctx, input: Option(str, "input:", required=True)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.price_check(ctx, input, is_response=True)

    async def price_check(self, ctx, input: Optional[str] = None, is_response: bool = False) -> None:
        closest = await smarter_find_closest(ctx, input, is_response=is_response)
        if closest is None:
            return
      
        if closest[0] == "enchant":
            enchant_type, level = closest[1].split(":")
            response = requests.get(f"https://sky.coflnet.com/api/item/price/ENCHANTED_BOOK?Enchantment={enchant_type}&EnchantLvl={level}").json()
            item_name = f"{enchant_type.replace('_', ' ').title()} {level} book"
        elif closest[0] == "pet":
            pet_type, rarity, level = closest[1].split(":")
            rarity_selector = "" if rarity == "None" else f"Rarity={rarity.upper()}"
            level_selector = "" if level == "None" else f"PetLevel={level}"
            if level != "None" and rarity != "None":
                level_selector = "&"+level_selector
            response = requests.get(f"https://sky.coflnet.com/api/item/price/PET_{pet_type.upper()}?{rarity_selector}{level_selector}").json()
            item_name = f"{pet_type.replace('_', ' ').title()}"
        elif closest[0] == "item":
            closest = closest[1]
            response = requests.get(f"https://sky.coflnet.com/api/item/price/{closest['internal_name']}").json()
            item_name = closest['name']

        if "Slug" in response.keys() or "min" not in response.keys():
            return await error(ctx, "Error, no items of that type could be found on the auction house!", "If you're searching for a pet, please end your search with 'pet', and if you're searching for an ultimate enchantment, please include `ultimate`.", is_response=is_response)

        string = [f"{MATHS_EMOJIS['min']} Minimum: {hf(response['min'])}",
                  f"{MATHS_EMOJIS['max']} Maximum: {hf(response['max'])}",
                  f"{MATHS_EMOJIS['volume']} Number sold: {hf(response['volume'])}",
                  f"{MATHS_EMOJIS['median']} Median: {hf(response['median'])}",
                  f"{MATHS_EMOJIS['mode']} Mode: {hf(response['mode'])}",
                  f"{MATHS_EMOJIS['mean']} Mean Average: {hf(response['mean'])}",
                  f"",
                  f"Links: Definitions for mode, median and mean: [link](https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/mean-median-basics/a/mean-median-and-mode-review), API: [link](https://sky.coflnet.com/data)"]
                    
        embed = discord.Embed(title=f"Price data found for {item_name}:", description="\n".join(string), colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)

