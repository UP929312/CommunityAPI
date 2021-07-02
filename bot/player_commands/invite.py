import discord
from discord.ext import commands

class invite_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title=f"Want to invite this bot to your server?", description=f"Go to [this link](https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=2147601408&scope=bot) and enjoy all the awesome features. Default prefix is `.` but can be changed with `.set_prefix`.", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
