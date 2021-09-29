import discord  # type: ignore
from discord.ext import commands  # type: ignore
from typing import Optional

from utils import error, ITEMS
from difflib import SequenceMatcher

class wiki_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(aliases=['wiki_link', 'wiki_links'])
    async def wiki(self, ctx, *, user_input: Optional[str] = None) -> None:

        if user_input is None:
            return await error(ctx, "No item given.", f"Please give the item you want to find the wiki page on.\nExample usage: {ctx.prefix}wiki Talisman Of Coins")

        # Get the closest match between your input and all the names
        closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, user_input.lower(), item["name"].lower()).ratio())
                
        if SequenceMatcher(None, user_input.lower(), closest["name"].lower()).ratio() < 0.6:
            # No item was found
            return await error(ctx, "No wiki entry with the provided input!", "Try being more accurate, and exclude special characters.")
                
        # Everything is fine, send it
        embed = discord.Embed(title=f"Wiki entry for {closest['name']}:", description=f"You can find the wiki entry [here]({closest['wiki_link']}).", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
