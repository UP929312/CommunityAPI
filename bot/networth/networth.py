import discord  # type: ignore
from discord.ext import commands  # type: ignore

from typing import Optional

import requests

from utils import error
from menus import generate_static_preset_menu
from database_manager import insert_profile
from parse_profile import get_profile_data
from networth.generate_page import generate_page
from networth.constants import PAGES, EMOJI_LIST

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()
        
class networth_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(aliases=["nw", "n", "net", "worth", "now", "new"])
    async def networth(self, ctx: commands.Context, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None) -> None:
        #=======================
        # Convert username/linked_account/nick to profile and more 
        player_data = await get_profile_data(ctx, provided_username, provided_profile_name, return_profile_list=True)
        if player_data is None:
            return None
        username, uuid, profile_data, profile_name = player_data["data"]
        #=======================
        # Make the API request
        try:
            request: requests.models.Response = requests.post(f"http://{self.client.ip_address}:8000/pages/{uuid}?profile_name={profile_name}", json=profile_data)
        except Exception as e:
            print(e)
            return await error(ctx, "Error, the bot could not connect to the API", "This could be because the API is down for maintenance, because it's restarting, or because there are issues. Try again later.")
        #=======================
        # Deal with exceptions
        if request.status_code == 500:
            return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
        elif request.status_code == 401:
            return await error(ctx, "Error, invalid profile given!", "Make sure it's one of their active profiles and try again.")
        elif request.status_code == 423:
            return await error(ctx, "Error, rate limit hit", "Your request has not been fufiled, please slow down and try again later.")            
        elif request.status_code == 404:
            return await error(ctx, "Error, that person could not be found", "Perhaps you input the incorrect name?")
        #=======================
        data = request.json()

        # Generate all the pages and initiate the menu handler
        list_of_embeds = [generate_page(ctx.author, data, username, page) for page in PAGES]        
        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, alternate_colours=True)

        # Add the data to the database (for the leaderboard command)
        data_totals: list[int] = [data[page]['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
        insert_profile(uuid, data["profile_data"]["profile_name"], data["profile_data"]["profile_type"], *data_totals)
