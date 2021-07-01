import discord
from discord.ext import commands

data_dict = {
    "nw": ("[username]", "Checks the total value of a profile for a user"),
    "set_prefix": ("<prefix>", "Allows an admin to change the prefix of the bot"),
    "ah": ("[username]", "Shows someone's active auctions (Coming soon)"),
    "bazaar": ("<item>", "Shows the bazaar price for a certain item, e.g. cobblestone (Coming soon)"),
    "dungeons": ("[username]", "Shows data about someone's dungeon level, including what floors they've beaten (Coming soon)"),
    "kills": ("[username]", "Shows the most mobs a player has killed (Coming soon)"),
    "skills": ("[username]", "Shows a summary of all a users skills, including average (Coming Soon)"),
    "slayer": ("[username]", "Shows a summary of someone's slayer data, including how many of each tier someone's killed (Coming soon)"),
    "wiki": ("[wiki page]", "Shows a page from the Hypixel wiki, to assist in finding a page or item."),
    }

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["h", "he", "hel"])
    async def help(self, ctx):
        embed = discord.Embed(title="Help command", colour=0x3498DB)
        for command, extras in data_dict.items():
            params, description = extras
            embed.add_field(name=f"{command} {params}", value=description, inline=False)
            
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
