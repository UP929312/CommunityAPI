import discord
from discord.ext import commands

import requests

from utils import error
from database_manager import insert_profile
from networth.generate_page import generate_page
from networth.constants import *
from parse_profile import input_to_uuid

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

PROFILE_NAMES = ['apple', 'banana', 'blueberry', 'coconut', 'cucumber', 'grapes', 'kiwi', 'lemon', 'lime', 'mango', 'orange', 'papaya', 'peach', 'pear', 'pineapple', 'pomegranate', 'raspberry', 'strawberry', 'tomato', 'watermelon', 'zucchini']

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
    async def networth(self, ctx, username=None, profile_name=None):
        # If they want to use auto-name and give a profile
        if username is not None and username.lower() in PROFILE_NAMES:
            profile_name = username
            username = None
        # Convert username/linked_account/nick to uuid
        data = await input_to_uuid(ctx, username)
        if data is None:
            return None
        username, uuid = data
    
        username, uuid = await input_to_uuid(ctx, username)
        if username is None:
            return

        #=======================
        # Get their profile data

        profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
        if profile_data in [None, {'success': True, 'profiles': None}]:
            return await error(ctx, "Error, that person has no profiles!", "The given person wasn't found on any profiles!")
        #=======================
        # Make the API request
        try:
            request = requests.post(f"http://{self.client.ip_address}:8000/pages/{uuid}?profile_name={profile_name}", json=profile_data)
        except Exception as e:
            print(e)
            return await error(ctx, "Error, the bot could not connect to the API", "This could be because the API is down for maintenance, because it's restarting, or because there are issues. Try again later.")

        #=======================
        # Deal with exceptions
        
        if request.status_code == 500:
            return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
        elif request.status_code == 401:
            return await error(ctx, "Error, invalid profile given!", "Make sure it's one of their active profiles and try again.")
        #elif request.status_code == 402:
        #    return await error(ctx, "Error, that person has no profiles!", "The given person wasn't found on any profiles!")
        elif request.status_code == 423:
            return await error(ctx, "Error, rate limit hit", "Your request has not been fufiled, please slow down and try again later.")            
        elif request.status_code == 404:
            return await error(ctx, "Error, that person could not be found", "Perhaps you input the incorrect name?")
        #=======================
        data = request.json()

        if "purse" not in data:
            print(data)

        main_embed = generate_page(ctx.author, data, username, "main")
        
        view = MenuView(command_author=ctx.author, data=data, username=username)
        view.message = await ctx.send(embed=main_embed, view=view)        

        data = [data[page]['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
        insert_profile(uuid, *data)
