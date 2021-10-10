import discord  # type: ignore
from discord.ext import commands  # type: ignore

from utils import guild_ids

class invite_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="invite")
    async def invite_command(self, ctx) -> None:
        await self.invite(ctx, is_reponse=False)

    @commands.slash_command(name="invite", description="Shows info on inviting the bot", guild_ids=guild_ids)
    async def invite_slash(self, ctx):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.invite(ctx, is_response=True)

    #=========================================================================================================================================
    
    async def invite(self, ctx, is_response: bool = False) -> None:
        invite_link = "https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=242666032192&scope=bot%20applications.commands"
        topgg_link = "https://top.gg/bot/854722092037701643"
        embed = discord.Embed(title=f"Want to invite this bot to your server?", description=f"Go to [this link]({invite_link}) to invite the bot, or [this link]({topgg_link}) to see the top.gg page and enjoy all the awesome features. Default prefix is `.` but can be changed with `.set_prefix`.", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
