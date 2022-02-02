import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

from database_manager import *
from utils import error, bot_can_send, guild_ids

class link_account_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="link_account", aliases=["linkaccount", "link"])
    async def link_account_command(self, ctx, username: Optional[str] = None) -> None:
        await self.link_account(ctx, username, is_response=False)

    @commands.slash_command(name="link_account", description="Links your discord account to a minecraft account", guild_ids=guild_ids)
    async def link_account_slash(self, ctx, username: Option(str, "username:", required=True)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.link_account(ctx, username, is_response=True)

    #==================================================================================================================

    async def link_account(self, ctx, username: Optional[str] = None, is_response: bool = False) -> None:
        if username is None:
            return await error(ctx, "Command link_account must have a username!", f"Example usage: `{ctx.prefix}link_account Notch`", is_response=is_response)
        if not (3 < len(username) <= 16):
            return await error(ctx, "Error, invalid username set!", "The username given must be a valid minecraft account!", is_response=is_response)
        
        current_linked_account: Optional[str] = self.client.linked_accounts.get(f"{ctx.author.id}", None)

        if current_linked_account is None:
            set_linked_account(ctx.author.id, username)
        else:
            update_linked_account(ctx.author.id, username)

        self.client.linked_accounts[f"{ctx.author.id}"] = username        

        embed = discord.Embed(title=f"Your linked account for Community Bot has been updated.", description=f"{ctx.author.display_name} has updated their linked account for community bot, it's now `{username}`", colour=0xe67e22)
        embed.set_footer(text=f"Use {'/' if is_response else ctx.prefix}link_account to change the account linked to Community Bot")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
