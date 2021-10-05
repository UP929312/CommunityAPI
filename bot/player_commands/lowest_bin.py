import discord  # type: ignore
from discord.ext import commands  # type: ignore
from typing import Optional

import requests
from datetime import datetime  # To convert hypixel time string to object

from utils import error, hf, format_duration, smarter_find_closest
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

    @commands.command(aliases=['lb', 'bin', 'lbin'])
    async def lowest_bin(self, ctx: commands.Context, *, input_item: Optional[str] = None) -> None:
        closest = await smarter_find_closest(ctx, input_item)
        if closest is None:
            return

        print(closest)

        if closest[0] == "enchant":
            enchant_type, level = closest[1].split(":")
            response = requests.get(f"https://sky-commands.coflnet.com/api/item/price/ENCHANTED_BOOK?Enchantment={enchant_type}&EnchantLvl={level}").json()
        elif closest[0] == "item":
            closest = closest[1]
            response = requests.get(f"https://sky.coflnet.com/api/auctions/tag/{closest['internal_name']}/active/bin").json()

        print("Response recieved")
        print(response)

        if not response or (isinstance(response, dict) and "Slug" in response.keys()):
            return await error(ctx, "Error, no items of that type could be found on the auction house!", "Try a different item instead?")

        list_of_embeds = []
        for page, data in enumerate(response, 1):
            #                                                                      # 2021-07-30T11:06:19Z
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
            
            formatted_auction = f"↳ Price: {hf(data['startingBid'])}\n↳ Time Remaining: {time_left}"+hot_potato_books+("\n" if not enchantments else enchantments)+f"\nTo view this auction ingame, type this command in chat:\n `/ah {data['auctioneerId']}`"
                
            embed = discord.Embed(title=f"Lowest bin found for {ITEM_RARITY[data['tier']]} {data['itemName']}, Page {page}:", description=formatted_auction, colour=0x3498DB)
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        

            list_of_embeds.append(embed)

        await generate_static_scrolling_menu(ctx=ctx, list_of_embeds=list_of_embeds)

