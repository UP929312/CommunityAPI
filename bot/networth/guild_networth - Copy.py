import discord
from discord.ext import commands

import requests

from utils import error
#from database_manager import insert_profile
from parse_profile import input_to_uuid
from networth.generate_page import generate_page
from networth.constants import *

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

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

def fetch_all_users(uuid_list):
    responses = []
    async with aiohttp.ClientSession() as session:
        for uuid in uuid_list:
            async with session.get(f"http://{self.client.ip_address}:8000/pages/{uuid}") as resp:
                responses.append(await resp.json())
        
class guild_networth_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["gnw", "gn"])
    async def guild_networth(self, ctx, username=None):
        username, uuid = await input_to_uuid(ctx, username)
        if uuid is None:
            return

        response = requests.get(f"https://api.hypixel.net/guild?key={API_KEY}&player={uuid}").json()
        
        members_uuid = [x['uuid'] for x in response['guild']['members']]
        username = response['guild']['name']

        responses = [requests.get(f"http://{self.client.ip_address}:8000/pages/{uuid}").json() for uuid in members_uuid]

        all_responses = {}
        master_response = {}
        master_response["purse"] = {"total": sum(int(x["purse"]["total"]) for x in responses)}
        master_response["banking"] = {"total": sum(int(x["banking"]["total"]) for x in responses)}
        
        for key in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
            all_responses[key] = {}
            #all_responses[key]["total"] = 0
            all_responses[key]["prices"] = []
            for response in responses:
                #all_responses[key]["total"] += int(response[key]["total"])
                all_responses[key]["prices"].extend(response[key]["prices"])

        #print(all_responses["inventory"][0])
        for key in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
            master_response[key] = {}
            master_response[key]["prices"] = sorted(all_responses[key]["prices"], key=lambda x: x["total"], reverse=True)[:5]
            master_response[key]["total"] = sum([x["total"] for x in master_response[key]["prices"]])
        
        main_embed = generate_page(ctx.author, master_response, username, "main")
        
        view = MenuView(command_author=ctx.author, data=master_response, username=username)
        view.message = await ctx.send(embed=main_embed, view=view)

        #uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]
        #data = [request.json()[page]['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
        #insert_profile(uuid, *data)
