import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests
from bisect import bisect

from parse_profile import get_profile_data
from utils import error, format_duration, clean, PROFILE_NAMES, guild_ids

def comma_seperate(num: float) -> str:
    return f"{int(num):,}"  # var:, = 10,000 (the comma)

class kills_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="kills", aliases=['k', 'kill'])
    async def kills_command(self, ctx, provided_username: Optional[str] = None, provided_profile: Optional[str] = None) -> None:
        await self.get_kills(ctx, provided_username, provided_profile, is_response=False)

    @commands.slash_command(name="kills", description="Gets the entities the player has killed the most", guild_ids=guild_ids)
    async def kills_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_kills(ctx, username, profile, is_response=True)

    #=========================================================================================================================================
        
    async def get_kills(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None, is_response: bool = False) -> None:
        
        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        stats = player_data["stats"]
        total_mobs_killed = f"**{comma_seperate(stats['kills'])}**" if "kills" in stats else "Unknown"  

        kills_stats = {k: v for k, v in stats.items() if k.startswith("kills_")}
        sorted_kills = dict(sorted(kills_stats.items(), key=lambda mob: mob[1], reverse=True)[:12])

        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

        embed.add_field(name=f"Kills Data", value=f"Total Mobs Killed {total_mobs_killed}", inline=False)

        for index, (key, value) in enumerate(sorted_kills.items(), 1):
            formatted_name = key.removeprefix("kills_").replace('_', ' ').title().replace('Unburried Zombie', 'Crypt Ghoul')
            embed.add_field(name=f"#{index} {formatted_name}", value=f":knife: {comma_seperate(value)}", inline=True)

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
