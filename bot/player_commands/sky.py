import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

from parse_profile import input_to_uuid

from utils import guild_ids

class sky_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="sky")
    async def sky_command(self, ctx, username: Optional[str] = None) -> None:
        await self.sky(ctx, username, is_response=False)

    @commands.slash_command(name="sky", description="Gets the sky link of the target", guild_ids=guild_ids)
    async def sky_slash(self, ctx, username: Option(str, "username:", required=False)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.sky(ctx, username, is_response=True)

    async def sky(self, ctx, provided_username: Optional[str] = None, is_response: bool = False) -> None:
        player_data: Optional[tuple[str, str]] = await input_to_uuid(ctx, provided_username, is_response=is_response)
        if player_data is None:
            return None
        username, uuid = player_data

        if is_response:
            await ctx.respond(f"https://sky.shiiyu.moe/stats/{username}")  # Send the link with the target's name
        else:
            await ctx.send(f"https://sky.shiiyu.moe/stats/{username}")  # Send the link with the target's name
