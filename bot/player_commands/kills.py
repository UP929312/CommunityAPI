import discord
from discord.ext import commands

import requests
from bisect import bisect

from parse_profile import get_profile_data

from utils import error, format_duration

class kills_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['k', 'kill'])
    async def kills(self, ctx, username=None):
        
        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        stats = player_data["stats"]
        total_mobs_killed = "**{:,}**".format(int(stats['kills'])) if "kills" in stats else "Unknown"

        kills_stats = {k: v for k, v in stats.items() if k.startswith("kills_")}
        sorted_kills = dict(sorted(kills_stats.items(), key=lambda mob: mob[1], reverse=True)[:12])

        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

        embed.add_field(name=f"Kills Data", value=f"Total Mobs Killed {total_mobs_killed}", inline=False)

        for index, (key, value) in enumerate(sorted_kills.items(), 1):
            formatted_name = key[6:].replace('_', ' ').title().replace('Unburried Zombie', 'Crypt Ghoul')
            embed.add_field(name=f"#{index} {formatted_name}", value=f":knife: {int(value)}", inline=True)

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
