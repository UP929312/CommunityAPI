import discord
from discord.ext import commands

from parse_profile import get_profile_data


class sky_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def sky(self, ctx, target=None):
        player_data = await get_profile_data(ctx, target)
        if player_data is None:
            return
        username = player_data["username"]
        
        await ctx.send(f"https://sky.shiiyu.moe/stats/{username}")  # Send the link with the target's name
