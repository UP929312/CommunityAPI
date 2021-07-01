import discord
from discord.ext import commands

from utils import *


class set_prefix_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.has_any_role("Administrator", "Admin", "Owner")
    @commands.command(aliases=["setprefix"])
    async def set_prefix(self, ctx, prefix=None):
        print("Setting prefix!")
        if prefix is None:
            return await error(ctx, "Command set_prefix must have a prefix", f"Example usage: `{ctx.prefix}set_prefix %`")
        if len(prefix) > 8:
            return await error(ctx, "Error, invalid prefix set!", "The prefix to start the community bot must be at most 8 characters long.")
        
        current_prefix = load_guild_prefix(ctx.guild.id)

        print(f"Current prefix: {current_prefix}, guild_id: {ctx.guild.id}, prefix: {prefix}")
        
        if current_prefix is None:
            set_guild_prefix(ctx.guild.id, prefix)
        else:
            update_guild_prefix(ctx.guild.id, prefix)

        embed = discord.Embed(title=f"The prefix for Community Bot has been updated.", description=f"{ctx.author.display_name} has updated the prefix for community bot, it's now triggered by `{prefix}`", colour=0xe67e22)
        embed.set_footer(text=f"Use set_prefix to change the prefix for Community Bot")        
        await ctx.send(embed=embed)
