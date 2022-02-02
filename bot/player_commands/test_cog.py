import discord
from discord.ext import commands
from discord.commands import Option

class test_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.slash_command(name="test", description="test_test", guild_ids=[854749884103917599])
    async def test_slash(self, ctx, username: Option(str, "username:", required=False, autocomplete=discord.utils.basic_autocomplete(values=["red", "green", "blue"])),
                                     profile: Option(str, "profile", choices=["Apple", "Banana"], required=False)):
        print(username, profile, is_response)
