import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional


from utils import PROFILE_NAMES, autocomplete_display_name

class test_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.slash_command(name="test", description="test_test", guild_ids=[854749884103917599])
    async def test_slash(self, ctx, username: Option(str, "username:", required=False, autocomplete=discord.utils.basic_autocomplete(values=["red", "green", "blue"])),
                                     profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        await self.do_test_slash(ctx, username, profile, is_response=True)

    async def do_test_slash(self, ctx, provided_username = None, provided_profile_name = None, is_response = False):
        print(provided_username, provided_profile_name, is_response)
