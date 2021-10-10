import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

from utils import error, ITEMS, guild_ids
from difflib import SequenceMatcher

class wiki_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="wiki", aliases=['wiki_link', 'wiki_links'])
    async def wiki_command(self, ctx, *, user_input: Optional[str] = None) -> None:
        await self.wiki(ctx, user_input, is_response=False)

    @commands.slash_command(name="wiki", description="Gets the wiki entry for an item", guild_ids=guild_ids)
    async def wiki_slash(self, ctx, item: Option(str, "item:", required=True)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.wiki(ctx, item, is_response=True)

    async def wiki(self, ctx, user_input: Optional[str] = None, is_response: bool = False) -> None:

        if user_input is None:
            return await error(ctx, "No item given.", f"Please give the item you want to find the wiki page on.\nExample usage: {ctx.prefix}wiki Talisman Of Coins", is_response=is_response)

        # Get the closest match between your input and all the names
        closest = max(ITEMS.values(), key=lambda item: SequenceMatcher(None, user_input.lower(), item["name"].lower()).ratio())
                
        if SequenceMatcher(None, user_input.lower(), closest["name"].lower()).ratio() < 0.6:
            # No item was found
            return await error(ctx, "No wiki entry with the provided input!", "Try being more accurate, and exclude special characters.", is_response=is_response)
                
        # Everything is fine, send it
        embed = discord.Embed(title=f"Wiki entry for {closest['name']}:", description=f"You can find the wiki entry [here]({closest['wiki_link']}).", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
