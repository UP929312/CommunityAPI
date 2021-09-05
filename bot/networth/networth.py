import discord
from discord.ext import commands

import requests

from utils import error
from database_manager import insert_profile
from networth.generate_page import generate_page
from networth.constants import *

ALLOWED_CHARS = {"_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

class MenuButton(discord.ui.Button['MenuView']):
    def __init__(self, page: str, index: int, disabled: bool):
        super().__init__(style=discord.ButtonStyle.grey if index%2==0 else discord.ButtonStyle.blurple, emoji=PAGE_TO_EMOJI[page], row=index//5, disabled=disabled)
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        view: MenuView = self.view
        if view.command_author.id == interaction.user.id or interaction.user.id == 244543752889303041:
            view.page = EMOJI_TO_PAGE[f"<:{self.emoji.name}:{self.emoji.id}>"]

            for child in self.view.children:
                child.disabled = False
            self.disabled = True
            
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
            self.add_item(MenuButton(page, index=i, disabled=i==0))

    async def update_embed(self, interaction: discord.Interaction):
        embed = generate_page(self.command_author, self.data, self.username, self.page)
        await interaction.response.edit_message(content="", view=self, embed=embed)

    async def on_timeout(self):
        try:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)
        except discord.errors.NotFound:
            print("Message to disable buttons on was deleted (/networth)")
        
class networth_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["nw", "n", "net", "worth", "now"])
    async def networth(self, ctx, username=None):

        if username is None:
            linked_account = self.client.linked_accounts.get(f"{ctx.author.id}", None)
            if linked_account:
                username = linked_account
            else:
                nick = ctx.author.display_name
                username = nick.split("]")[1] if "]" in nick else nick
                username = "".join([char for char in username if char.lower() in ALLOWED_CHARS])

        try:
            request = requests.get(f"http://{self.client.ip_address}:8000/pages/{username}")
        except Exception as e:
            print(e)
            return await error(ctx, "Error, the bot could not connect to the API", "This could be because the API is down for maintenance, because it's restarting, or because there are issues. Try again later.")

        if request.status_code == 500:
            return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
        elif request.status_code == 423:
            return await error(ctx, "Error, rate limit hit", "Your request has not been fuffiled, please slow down and try again later.")            
        elif request.status_code == 404:
            return await error(ctx, "Error, that person could not be found", "Perhaps you input the incorrect name?")
        elif request.status_code == 502:
            return await error(ctx, "Error, the API key was killed.", "Hypixel will randomly kill the API key, please be patient while a new key is generated.")
        elif request.status_code == 503:
            return await error(ctx, "Error, Mojang's servers are down!", "The bot couldn't properly exchange data with Mojang's servers, try using a UUID instead?")            

        main_embed = generate_page(ctx.author, request.json(), username, "main")
        
        view = MenuView(command_author=ctx.author, data=request.json(), username=username)
        view.message = await ctx.send(embed=main_embed, view=view)

        if len(username) > 16:
            uuid = username
        else:
            uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]
        data = [request.json()[page]['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
        insert_profile(uuid, *data)
