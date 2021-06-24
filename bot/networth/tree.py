import discord
from discord.ext import commands

import requests
from io import StringIO

from utils import error

class tree_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    # discord staff, Admin, Booster, Donator 10$, giveaway contri, don 50, 20, 30
    #@commands.has_any_role(701205423742648350, "Admin", 591691127694819350, 784041616444882954, 743950132931723349, 794541062134824971, 793070309213208606, 793070744829296670)
    @commands.command()
    async def tree(self, ctx, username=None):

        if username is None:
            nick = ctx.author.nick
            username = nick.split("]")[1] if "]" in nick else nick
            
        try:
            request = requests.get(f"http://{self.client.ip_address}:8000/tree/{username}")
        except Exception as e:
            print(e)
            return await error(ctx, "Error, the bot could not connect to the API", "This could be because the API is down for maintenance, because it's restarting, or because there are issues. Try again later.")
        
        if request.status_code != 200:
            if request.status_code >= 500:  # Over 500 = Server fails
                return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
            if request.status_code != 400:  # !400 = Meh
                return await error(ctx, "Error, no connection", "The bot couldn't connect to the API, it may be down or failing")
            # 400 = Username not found
            return await error(ctx, "Error, that person could not be found", f"Perhaps you input the incorrect name? Status code: {request.status_code}")

        string_io = StringIO()
        string_io.write(request.json())
        string_io.seek(0)
        file = discord.File(string_io, filename=f"{username}_dump.txt")

        await ctx.send(file=file)
