import discord
from discord.ext import commands


ALLOWED_CHARS = {"_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

class sky_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def sky(self, ctx, target=None):
        if target is None:  # If they don't give any args, use their discord nick 
            nick = ctx.author.display_name  #  Set nick to their author of the command's nickname
            target = nick.split("]")[1] if "]" in nick else nick  # If the nickname contains a ], get all the characters after the ]
            target = "".join([char for char in target if char.lower() in ALLOWED_CHARS])  # Create a new string with only the allowed characters (0-9, A-Z, _)

        await ctx.send(f"https://sky.shiiyu.moe/stats/{target}")  # Send the link with the target's name
