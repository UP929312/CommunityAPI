import discord
from discord.ext import commands

class invite_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def invite(self, ctx):
        invite_link = "https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=242666032192&scope=bot%20applications.commands"
        topgg_link = "https://top.gg/bot/854722092037701643"
        embed = discord.Embed(title=f"Want to invite this bot to your server?", description=f"Go to [this link]({invite_link}) to invite the bot, or [this link]({topgg_link}) to see the top.gg page and enjoy all the awesome features. Default prefix is `.` but can be changed with `.set_prefix`.", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
