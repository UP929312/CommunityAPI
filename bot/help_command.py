import discord
from discord.ext import commands

data_dict = {
    "nw": ("[username]", "Checks the total value of a profile for a user."),
    "ah": ("[username]", "Shows someone's auctions and BINs."),
    "bazaar": ("<item>", "Shows the bazaar price for a certain item, e.g. 'cobblestone'."),
    "dungeons": ("[username]", "Shows data about someone's dungeon level, including what floors they've beaten."),
    "kills": ("[username]", "Shows the most mobs a player has killed."),
    "missing": ("[username]", "Shows the top tier talisman that the player is missing."),
    "set_prefix": ("<prefix>", "Allows an admin to change the prefix of the bot."),
    "skills": ("[username]", "Shows a summary of all a users skills, including average."),
    "sky": ("[username]", "Links you to someone's sky.shiiyu.moe page, for convenience."),
    "slayer": ("[username]", "Shows a summary of someone's slayer data, including how many of each tier someone's killed."),
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
