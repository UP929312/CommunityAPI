import discord
from discord.ext import commands

from utils import error, get_master_accessories
from parse_profile import get_profile_data

MASTER_ACCESSORIES = get_master_accessories()

class missing_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['missing_accessories', 'accessories', 'miss', 'm'])
    async def missing(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        missing = [x for x in MASTER_ACCESSORIES if x not in player_data["accessories"]
        accessory_names = sorted([ACCESSORY_ID_TO_HUMAN_NAME[x] for x in missing])

        embed = discord.Embed(title=f"Missing {len(missing)} accessories for {username}", description=("\n".join(accessory_names))[:3500], colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)

