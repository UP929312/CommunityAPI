import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

from database_manager import *
from utils import error

class set_prefix_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_prefix", aliases=["setprefix"])
    async def set_prefix_command(self, ctx, prefix: Optional[str] = None) -> None:

        is_response = False ###############################################

        print(f"------ Request made in from guild: {ctx.guild.id if ctx.guild is not None else 'DMs'}, from user: {ctx.author.id}, sometimes known as {ctx.author.display_name}\nThey set their guild/dm prefix to {prefix}")
         
        if prefix is None:
            return await error(ctx, "Command set_prefix must have a prefix", f"Example usage: `{ctx.prefix}set_prefix %`", is_response=is_response)
        if len(prefix) > 8:
            return await error(ctx, "Error, invalid prefix set!", "The prefix to start the community bot must be at most 8 characters long.", is_response=is_response)
        
        current_prefix = self.client.prefixes.get(f"{ctx.guild.id}", None)

        if current_prefix is None:
            set_guild_prefix(ctx.guild.id, prefix)
        else:
            update_guild_prefix(ctx.guild.id, prefix)

        self.client.prefixes[f"{ctx.guild.id}"] = prefix
        
        embed = discord.Embed(title=f"The prefix for Community Bot has been updated.", description=f"{ctx.author.display_name} has updated the prefix for community bot, it's now triggered by `{prefix}`", colour=0xe67e22)
        embed.set_footer(text=f"Use set_prefix to change the prefix for Community Bot")        
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
