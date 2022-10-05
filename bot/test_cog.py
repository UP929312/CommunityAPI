import discord
from discord.ext import commands
from discord.commands import Option
from discord.ui import InputText, Modal

class MyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(
            InputText(
                label="Short Input",
                placeholder="Placeholder Test"
            )
        )
        print("Here")

        self.add_item(
            InputText(
                label="Longer Input",
                value="Longer Value\nSuper Long Value",
                style=discord.InputTextStyle.long,
                placeholder="Placeholder",
                row=0
            )
        )
        print("Here2")
        
    async def callback(self, interaction):
        embed = discord.Embed(title="Your Modal Results")
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])

class test_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    '''
    @commands.slash_command(name="test", description="test_test", guild_ids=[854749884103917599])
    async def test_slash(self, ctx, username: Option(str, "username:", required=False, autocomplete=discord.utils.basic_autocomplete(values=["red", "green", "blue"])),
                                     profile: Option(str, "profile", choices=["Apple", "Banana"], required=False)):
        print(username, profile, is_response)
    '''
    @commands.slash_command(name="test", description="test_test", guild_ids=[854749884103917599])  # CB
    async def test_slash(self, ctx):
        #embed = discord.Embed(description="Testing modalds", colour=0x3498DB)
        #await embed.send()
        print("We're here")

        modal = MyModal(title="Slash Command Modal")
        await ctx.interaction.response.send_modal(modal)
        
        
