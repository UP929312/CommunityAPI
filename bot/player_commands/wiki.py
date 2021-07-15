import discord
from discord.ext import commands

import json
from difflib import SequenceMatcher

from utils import error


with open("text_files/cleaned_items.txt", "r") as file:
    WIKI_ENTRIES = json.load(file)

class wiki_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['wiki_links'])
    async def wiki(self, ctx, *, user_input=None):

        if user_input is None:
            return await error(ctx, "No item given.", "Please give the item you want to check the price of.")
        
        formatted_id = user_input.replace(" ", "_").replace("- ", "").upper()

        top_similarity_ration = 0
        for name, entry in WIKI_ENTRIES.items():
            similarity_ratio = SequenceMatcher(None, formatted_id, name).ratio()
            if similarity_ratio > top_similarity_ration:
                top_similarity_ration = similarity_ratio
                wiki_entry = entry
                
        if top_similarity_ration < 0.6:
            # Nobreak: Item was no found, show exceptions
            return await error(ctx, "No wiki entry with the provided input!", "Try giving the internal item name, and exclude special characters.")
                
        # Everything is fine, send it
        embed = discord.Embed(title=f"Wiki entry for {formatted_id.replace('_', ' ').title()}:", description=f"You can find the wiki entry [here]({wiki_entry}).", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
