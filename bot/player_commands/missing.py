import discord
from discord.ext import commands
import json

from utils import error
from emojis import ITEM_RARITY
from parse_profile import get_profile_data
from extract_ids import extract_internal_names

# Create the master list!
from text_files.accessory_list import talisman_upgrades

# Get a list of all accessories
ACCESSORIES = []
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

class missing_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['missing_accessories', 'accessories', 'miss', 'm'])
    async def missing(self, ctx, username=None, profile=None):

        player_data = await get_profile_data(ctx, username, profile)
        if player_data is None:
            return
        username = player_data["username"]

        accessory_bag = player_data.get("talisman_bag", None)
        inv_content = player_data.get("inv_contents", {"data": []})
        
        if not accessory_bag:
            return await error(ctx, "Error, could not find this person's accessory bag", "Do they have their API disabled for this command?")

        accessory_bag = extract_internal_names(accessory_bag["data"])
        inventory = extract_internal_names(inv_content["data"])

        missing = [x for x in MASTER_ACCESSORIES if x["internal_name"] not in accessory_bag+inventory]

        if not missing:
            return await error(ctx, f"Completion!", f"{username} already has all accessories!")
        sorted_accessories = sorted(missing, key=lambda x: x["name"])[:42]

        extra = "" if len(missing) <= 36 else f", showing the first {len(sorted_accessories)}"
        embed = discord.Embed(title=f"Missing {len(missing)} accessories for {username}{extra}", colour=0x3498DB)

        def make_embed(embed, acc_list):
            text = ""
            for item in acc_list:
                internal_name, name, rarity, wiki_link, _ = item.values()
                wiki_link = "<Doesn't exist>" if not wiki_link else f"[wiki]({wiki_link})"
                text += f"{ITEM_RARITY[rarity]} {name}\nLink: {wiki_link}\n"
                            
            embed.add_field(name=f"{acc_list[0]['name'][0]}-{acc_list[-1]['name'][0]}", value=text, inline=True)
            
        if len(sorted_accessories) < 6:  # For people with only a few missing
            make_embed(embed, sorted_accessories)
        else:
            list_length = int(len(sorted_accessories)/6)
            for row in range(6):
                row_accessories = sorted_accessories[row*list_length:(row+1)*list_length]  # Get the first group out of 6
                make_embed(embed, row_accessories)

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)

