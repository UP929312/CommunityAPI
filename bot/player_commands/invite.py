import discord  # type: ignore
from discord.ext import commands  # type: ignore

from utils import guild_ids

'''
def check():      
    async def predicate(ctx):
        print((ctx.channel.permissions_for(ctx.guild.me)).send_messages)
        return (ctx.channel.permissions_for(ctx.guild.me)).send_messages
    
    return commands.check(predicate)
#'''
'''
def custom_check():
    print("Check!")
    print((ctx.channel.permissions_for(ctx.guild.me)).send_messages)
    return (ctx.channel.permissions_for(ctx.guild.me)).send_messages
#'''

'''
def allowed_channels(allowed_channels_list):      
    async def predicate(ctx):
        return ctx.guild and (ctx.channel.id in allowed_channels_list)
    return commands.check(predicate)

@allowed_channels([PREFIX_COMMAND])
'''

class invite_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="invite")
    async def invite_command(self, ctx) -> None:
        await self.invite(ctx, is_response=False)

    #@check()
    #@commands.has_permissions(send_messages=True)
    @commands.slash_command(name="invite", description="Shows info on inviting the bot", guild_ids=guild_ids)#, checks=[check,])
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
