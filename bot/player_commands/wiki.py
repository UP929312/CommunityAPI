import discord
from discord.ext import commands

import json
from difflib import SequenceMatcher

from utils import error

with open("text_files/MASTER_ITEM_DICT.json", "r", encoding="utf-8") as file:
    WIKI_ENTRIES = json.load(file)

class wiki_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['wiki_links'])
    async def wiki(self, ctx, *, user_input=None):

        if user_input is None:
            return await error(ctx, "No item given.", f"Please give the item you want to check the price of.\nExample usage: {ctx.prefix}wiki Talisman Of Coins")

        # Get the closest match between your input and all the names
        closest = max(WIKI_ENTRIES.values(), key=lambda item: SequenceMatcher(None, user_input, item["name"]))
                
        if similar(user_input, closest["name"]) < 0.6:
            # No item was found
            return await error(ctx, "No wiki entry with the provided input!", "Try giving the internal item name, and exclude special characters.")
                
        # Everything is fine, send it
        embed = discord.Embed(title=f"Wiki entry for {closest['name'].replace('_', ' ').title()}:", description=f"You can find the wiki entry [here]({wiki_entry}).", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
