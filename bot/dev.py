import discord
from discord.ext import commands

OPTIONS = ["Paris", "London", "Tokyo", "New York", "Warsaw"]


class StaticPresetMenuButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(style=discord.ButtonStyle.blurple, label=label)


class StaticPresetMenuView(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.options = options

        for option in options:
            self.add_item(StaticPresetMenuButton(label=option))

async def generate_static_preset_menu(ctx, embed, options):
    await ctx.send(embed=embed, view=StaticPresetMenuView(options=options))


class dev_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="dev")
    async def dev_command(self, ctx):
        embed = discord.Embed(title=f"Question number 5", description="In the year 987 A.D, currently with 67 million people, what city was made to be the capital of France?", colour=0x3498DB)
        embed.set_footer(text=f"Quiz hosted by @DrMatt")

        await generate_static_preset_menu(ctx, embed, OPTIONS)
