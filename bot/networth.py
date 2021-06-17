import discord
from discord.ext import commands

import requests

from utils import error
from generate_page import generate_page
from constants import *

with open("api_address.txt") as file:
    ip = file.read()


class MenuButton(discord.ui.Button['MenuView']):
    def __init__(self, page: str, index: int):
        super().__init__(style=discord.ButtonStyle.secondary if index%2==0 else discord.ButtonStyle.primary, emoji=PAGE_TO_EMOJI[page], row=index//5)
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        view: MenuView = self.view
        if view.command_author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = EMOJI_TO_PAGE[f"<:{self.emoji.name}:{self.emoji.id}>"]
            await self.view.update_embed(interaction)
        else:
            await interaction.response.send_message("This isn't your command!\nYou can run this command yourself to change the pages!", ephemeral=True)
        

class MenuView(discord.ui.View):
    def __init__(self, command_author, data, username: str):
        super().__init__()
        self.command_author = command_author
        self.page = "inventory"
        self.data = data
        self.username = username

        for i, page in enumerate(page_names):
            self.add_item(MenuButton(page, index=i))

    async def update_embed(self, interaction: discord.Interaction):
        embed = generate_page(self.command_author, self.data, self.username, self.page)
        await interaction.response.edit_message(content="", view=self, embed=embed)

        
class networth_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    # discord staff, Admin, Booster, Donator 10$, giveaway contri, don 50, 20, 30
    @commands.command(aliases=["nw", "n", "net", "worth"])
    @commands.has_any_role(701205423742648350, "Admin", 591691127694819350, 784041616444882954, 743950132931723349, 794541062134824971, 793070309213208606, 793070744829296670)
    async def networth(self, ctx, username=None):

        if username is None:
            nick = ctx.author.nick
            username = nick.split("]")[1] if "]" in nick else nick

        request = requests.get(f"http://127.0.0.1:8000/pages/{username}")
        if request.status_code != 200:
            if request.status_code >= 500:  # Over 500 = Server fails
                return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
            if request.status_code != 400:  # !400 = Meh
                return await error(ctx, "Error, no connection", "The bot couldn't connect to the API, it may be down or failing")
            # 400 = Username not found
            return await error(ctx, "Error, that person could not be found", "Perhaps you input the incorrect name?")

        main_embed = generate_page(ctx.author, request.json(), username, "main")
        await ctx.send(embed=main_embed, view=MenuView(command_author=ctx.author, data=request.json(), username=username))
