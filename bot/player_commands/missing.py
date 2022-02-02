import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import json
import requests

from utils import error, PROFILE_NAMES, hf, bot_can_send, guild_ids
from menus import generate_static_preset_menu
from emojis import ITEM_RARITY
from parse_profile import get_profile_data
from extract_ids import extract_internal_names

RARITY_LIST = list(ITEM_RARITY.keys())

# Create the master list!
from text_files.accessory_list import talisman_upgrades

# Get a list of all accessories
ACCESSORIES: list[dict] = []
with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    item_dict = json.load(file)
    for item in item_dict:
        if item_dict[item].get("rarity", False) and item_dict[item]["rarity"] != "UNKNOWN":
            ACCESSORIES.append(item_dict[item])

# Now remove all the low tier ones
MASTER_ACCESSORIES = []
for accessory in ACCESSORIES:
    if accessory["internal_name"] not in talisman_upgrades.keys():
        MASTER_ACCESSORIES.append(accessory)

EMOJI_LIST = ["<:alphabetically:905066318720544779>", "<:recombobulator:854750106376339477>", "<:by_price:900069290143797299>"]

class missing_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="missing", aliases=['missing_accessories', 'accessories', 'miss', 'm'])
    async def missing_command(self, ctx, provided_username: Optional[str] = None, provided_profile: Optional[str] = None) -> None:
        await self.get_missing(ctx, provided_username, provided_profile, is_response=False)

    @commands.slash_command(name="missing", description="Gets someone's missing accessories", guild_ids=guild_ids)
    async def missing_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_missing(ctx, username, profile, is_response=True)

    #=========================================================================================================================================
        
    async def get_missing(self, ctx, provided_username: Optional[str] =  None, provided_profile_name: Optional[str] =  None, is_response: bool = False) -> None:

        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        accessory_bag = player_data.get("talisman_bag", None)
        inv_content = player_data.get("inv_contents", {"data": []})
        
        if not accessory_bag:
            return await error(ctx, "Error, could not find this person's accessory bag", "Do they have their API disabled for this command?", is_response=is_response)

        accessory_bag = extract_internal_names(accessory_bag["data"])
        inventory = extract_internal_names(inv_content["data"])

        missing = [x for x in MASTER_ACCESSORIES if x["internal_name"] not in accessory_bag+inventory]

        if not missing:
            return await error(ctx, f"Completion!", f"{username} already has all accessories!", is_response=is_response)

        try:
            lowest_bin_data = requests.get("http://moulberry.codes/lowestbin.json").json()
        except:
            return await error(ctx, f"Error, price API is down!", f"Please wait for it to return, and try again later!", is_response=is_response)

        for accessory in missing:
            accessory["price"] = lowest_bin_data.get(accessory["internal_name"], 9999999999)

        list_of_embeds = []

        for page, parameter in zip(["alphabetically", "by rarity", "by price"], ["name", "rarity", "price"]):
            sort_func = lambda x: x[parameter] if parameter != "rarity" else RARITY_LIST.index(x["rarity"])
            sorted_accessories = sorted(missing, key=sort_func)[:42]
                            
            extra = "" if len(missing) <= 36 else f", showing the first {int(len(sorted_accessories)/6)}"
            embed = discord.Embed(title=f"Missing {len(missing)} accessories for {username}{extra}, sorted: {page}", colour=0x3498DB)

            def make_embed(embed, acc_list, num):
                text = ""
                for item in acc_list:
                    wiki_link = "<Unknown>" if not item['wiki_link'] else f"[wiki]({item['wiki_link']})"
                    price = hf(item['price']) if item['price'] != 9999999999 else 'N/A'
                    text += f"{ITEM_RARITY[item['rarity']]} {item['name']}\n➜ For {price}, link: {wiki_link}\n"

                embed_title = f"{acc_list[0]['name'][0]}-{acc_list[-1]['name'][0]}" if parameter == "name" else f"Group {num}"
                embed.add_field(name=f"{embed_title}", value=text, inline=True)
                
            if len(sorted_accessories) < 6:  # For people with only a few missing
                make_embed(embed, sorted_accessories, 1)
            else:
                list_length = int(len(sorted_accessories)/6)
                for row in range(6):
                    row_accessories = sorted_accessories[row*list_length:(row+1)*list_length]  # Get the first group out of 6
                    make_embed(embed, row_accessories, row+1)

            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

            list_of_embeds.append(embed)
        
        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, is_response=is_response)

