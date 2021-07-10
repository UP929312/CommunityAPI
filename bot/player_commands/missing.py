import discord
from discord.ext import commands

from text_files.master_accessories import MASTER_ACCESSORIES
from utils import error
from parse_profile import get_profile_data
from extract_ids import parse_container

RARITY_DICT = {   
    "COMMON":    "<:common:863390433593786369>",
    "UNCOMMON":  "<:uncommon:863390433517895690>",
    "RARE":      "<:rare:863390433186152459>",
    "EPIC":      "<:epic:863390433526022165>",
    "LEGENDARY": "<:legendary:863390433493123072> ",
}

class missing_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['missing_accessories', 'accessories', 'miss', 'm'])
    async def missing(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        accessory_bag = player_data.get("talisman_bag", None)
        inv_content = player_data.get("inv_contents", {"data": []})
        
        if not accessory_bag:
            return await error(ctx, "Error, could not find this person's accessory bag", "Do they have their API disabled for this command?")

        accessory_bag = parse_container(accessory_bag["data"])
        inventory = parse_container(inv_content["data"])

        missing = [x for x in MASTER_ACCESSORIES if x[0] not in accessory_bag+inventory]

        if not missing:
            return await error(ctx, f"Completion!", f"{username} already has all accessories!")
        sorted_accessories = sorted(missing, key=lambda x: x[1])[:42]

        extra = "" if len(missing) <= 36 else f", showing top {len(sorted_accessories)}"
        embed = discord.Embed(title=f"Missing {len(missing)} accessories for {username}{extra}", colour=0x3498DB)

        if len(sorted_accessories) < 6:  # For people with only a few missing
            text = ""
            for _, name, rarity, wiki_link in sorted_accessories:
                text += f"{RARITY_DICT[rarity]} {name}\nLink: [here]({wiki_link})\n" 
            embed.add_field(name=f"{sorted_accessories[0][1][0]}-{sorted_accessories[-1][1][0]}", value=text, inline=True) 
        else:
            list_length = int(len(sorted_accessories)/6)
            for row in range(6):
                row_accessories = sorted_accessories[row*list_length:(row+1)*list_length]  # Get the first group out of 6
                text = ""
                for accessory in row_accessories:
                    _, name, rarity, wiki_link = accessory
                    text += f"{RARITY_DICT[rarity]} {name}\nLink: [here]({wiki_link})\n"
                            
                embed.add_field(name=f"{row_accessories[0][1][0]}-{row_accessories[-1][1][0]}", value=text, inline=True) 

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)

