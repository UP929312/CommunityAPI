import discord
from discord.ext import commands

from database_manager import get_saved_profiles
from parse_profile import get_profile_data
from utils import error

class graph_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["g", "plot"])
    async def graph(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]
        uuid = player_data["uuid"]

        records = get_saved_profiles(uuid)
        if len(records) < 5:
            return await error(ctx, "Error, this player doesn't have enough data", "For this command to work, there must be enough data to show, try running the command a few times later for it to properly show change!")

        embed = discord.Embed(title=f"Networth history for {username}", description=f"\n".join([", ".join(str(x) for x in records)]), colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
