import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests
from datetime import datetime  # To convert hypixel time string to object

from utils import error, hf, format_duration, smarter_find_closest, bot_can_send, guild_ids
from emojis import ITEM_RARITY
from menus import generate_static_scrolling_menu


def format_enchantments(enchantments: list[str]) -> str:
    if not enchantments:
        return ""
    sorted_enchants = sorted(enchantments, key=lambda ench: ench.startswith("Ultimate"), reverse=True)
    
    enchantment_pairs = [sorted_enchants[i:i + 2] for i in range(0, len(sorted_enchants), 2)]
    if len(enchantment_pairs[-1]) == 1:
        enchantment_pairs[-1] = (enchantment_pairs[-1][0], "")

    enchantment_string = "\n".join([f"[{first.replace('_', ' ')}, {second.replace('_', ' ')}]".replace(", ]", "]") for first, second in enchantment_pairs])

    formatted_enchants = f'''```ini
[Enchantments]
{enchantment_string}
```
'''.rstrip("\n")
    return formatted_enchants

class lowest_bin_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="lowest_bin", aliases=['lb', 'bin', 'lbin'])
    async def lowest_bin_command(self, ctx, *, input: Optional[str] = None) -> None:
        await self.lowest_bin(ctx, input, is_response=False)

    @commands.slash_command(name="lowest_bin", description="Gets the top 10 lowest BINs of that item on the AH", guild_ids=guild_ids)
    async def lowest_bin_slash(self, ctx, input: Option(str, "input:", required=True)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.lowest_bin(ctx, input, is_response=True)

    #===============================================================================================================

    async def lowest_bin(self, ctx, input: Optional[str] = None, is_response: bool = False) -> None:
        closest = await smarter_find_closest(ctx, input)
        if closest is None:
            return

        if closest[0] == "enchant":
            enchant_type, level = closest[1].split(":")
            response = requests.get(f"https://sky.coflnet.com/api/auctions/tag/ENCHANTED_BOOK/active/bin?Enchantment={enchant_type}&EnchantLvl={level}")
        elif closest[0] == "pet":
            pet_type, rarity, level = closest[1].split(":")
            rarity_selector = "" if rarity == "None" else f"Rarity={rarity.upper()}"
            level_selector = "" if level == "None" else f"PetLevel={level}"
            if level != "None" and rarity != "None":
                level_selector = "&"+level_selector
            response = requests.get(f"https://sky.coflnet.com/api/auctions/tag/PET_{pet_type.upper()}/active/bin?{rarity_selector}{level_selector}")
            
        elif closest[0] == "item":
            closest = closest[1]
            response = requests.get(f"https://sky.coflnet.com/api/auctions/tag/{closest['internal_name']}/active/bin")

        try:
            response = response.json()
        except Exception as e:
            print(response.status_code)
            print(e)
            print(response.text)

        if not response or (isinstance(response, dict) and "Slug" in response.keys()):
            return await error(ctx, "Error, no items of that type could be found on the auction house!", "If you're searching for a pet, please end your search with 'pet', and if you're searching for an ultimate enchantment, please include `ultimate`.", is_response=is_response)

        list_of_embeds = []
        for page, data in enumerate(response, 1):
            #   ->                                                                    # 2021-07-30T11:06:19Z
            time_left: str = format_duration(datetime.strptime(data['end'].rstrip("Z"), '%Y-%m-%dT%H:%M:%S'))

            # Enchants
            enchantment_list: list[str] = [x["type"].title()+f" {x['level']}" for x in data["enchantments"]]
            enchantments: str = format_enchantments(enchantment_list)
            # Hot potato books
            hot_potato_books: str = data["flatNbt"].get("hpc", "")
            if hot_potato_books:
                if int(hot_potato_books) > 10:
                    hot_potato_books = f"\n\nThis item has 10 hot potato books, and {int(hot_potato_books)-10} fuming potato books"
                else:
                    hot_potato_books = f"\n\nThis item has {hot_potato_books} hot potato books"

            # Format the auction
            formatted_auction = f"↳ Price: {hf(data['startingBid'])}\n↳ Time Remaining: {time_left}"+hot_potato_books+("\n" if not enchantments else enchantments)+f"\nTo view this auction ingame, type this command in chat:\n `/ah {data['auctioneerId']}`"
                
            embed = discord.Embed(title=f"Lowest bin found for {ITEM_RARITY[data['tier']]} {data['itemName']}, Page {page}:", description=formatted_auction, colour=0x3498DB)
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        

            list_of_embeds.append(embed)

        await generate_static_scrolling_menu(ctx=ctx, list_of_embeds=list_of_embeds, is_response=is_response)

