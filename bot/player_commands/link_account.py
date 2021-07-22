import discord
from discord.ext import commands

from database_manager import *
from utils import error

class link_account_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["linkaccount", "link"])
    async def link_account(self, ctx, username=None):

        if username is None:
            return await error(ctx, "Command link_account must have a username!", f"Example usage: `{ctx.prefix}link_account Notch`")
        if not (3 < len(username) < 16):
            return await error(ctx, "Error, invalid username set!", "The username given must be a valid minecraft account!")
        
        current_linked_account = self.client.linked_accounts.get(f"{ctx.author.id}", None)

        if current_linked_account is None:
            set_linked_account(ctx.author.id, username)
        else:
            update_linked_account(ctx.author.id, username)

        self.client.linked_accounts[f"{ctx.author.id}"] = username        

        embed = discord.Embed(title=f"Your linked account for Community Bot has been updated.", description=f"{ctx.author.display_name} has updated their linked account for community bot, it's now `{username}`", colour=0xe67e22)
        embed.set_footer(text=f"Use {ctx.prefix}link_account to change the account linked to Community Bot")        
        await ctx.send(embed=embed)
