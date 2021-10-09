import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

from parse_profile import input_to_uuid


class sky_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command()
    async def sky(self, ctx, provided_username: Optional[str] = None) -> None:

        is_response = False
        player_data: Optional[tuple[str, str]] = await input_to_uuid(ctx, provided_username, is_response=is_response)
        if player_data is None:
            return None
        username, uuid = player_data
        
        await ctx.send(f"https://sky.shiiyu.moe/stats/{username}")  # Send the link with the target's name
