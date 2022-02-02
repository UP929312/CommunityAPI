import discord  # type: ignore
from discord.ext import commands  # type: ignore

from typing import Optional

import aiohttp
import requests

from utils import error, bot_can_send
from menus import generate_static_preset_menu
from parse_profile import input_to_uuid
from networth.generate_page import generate_page
from networth.constants import PAGES, EMOJI_LIST

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

async def fetch_all_users_data(self, uuid_list: list[str]) -> list[dict]:
    responses = []
    async with aiohttp.ClientSession() as session:
        for uuid in uuid_list:
            async with session.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}") as resp:
                profile_data = await resp.json()
            async with session.post(f"http://{self.client.ip_address}:8000/pages/{uuid}", json=profile_data) as resp:
                responses.append(await resp.json())
    return responses
        
class guild_networth_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(aliases=["gnw", "gn"])
    async def guild_networth(self, ctx: commands.Context, provided_username: Optional[str] = None) -> None:
        username, uuid = await input_to_uuid(ctx, provided_username)
        if uuid is None:
            return

        response = requests.get(f"https://api.hypixel.net/guild?key={API_KEY}&player={uuid}").json()
        
        members_uuid = [x['uuid'] for x in response['guild']['members']]
        guild_name = response['guild']['name']

        responses = await fetch_all_users_data(self, members_uuid)

        all_responses, master_response = {}, {}
        master_response["purse"] = {"total": sum(int(x["purse"]["total"]) for x in responses)}
        master_response["banking"] = {"total": sum(int(x["banking"]["total"]) for x in responses)}
        
        for key in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
            all_responses[key] = {}
            all_responses[key]["prices"] = []
            for response in responses:
                all_responses[key]["prices"].extend(response[key]["prices"])

        for key in ("inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"):
            master_response[key] = {}
            master_response[key]["prices"] = sorted(all_responses[key]["prices"], key=lambda x: x["total"], reverse=True)[:5]
            master_response[key]["total"] = str(sum([x["total"] for x in all_responses[key]["prices"]]))

        # Generate all the pages and initiate the menu handler
        list_of_embeds = [generate_page(command_author=ctx.author, data=master_response, username=guild_name, page=page, use_guilds=True) for page in PAGES]
        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, alternate_colours=True)
