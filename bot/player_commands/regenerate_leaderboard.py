import discord  # type: ignore
from discord.ext import commands  # type: ignore

import requests

from database_manager import get_max_current_networth, insert_profile

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

class regenerate_leaderboard_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.is_owner()
    @commands.command(aliases=["rl"])
    async def regenerate_leaderboard(self, ctx) -> None:        
        records = get_max_current_networth("regular")

        for uuid, total in records:
            print(f"Re-calculated {uuid}")
            profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
            
            request = requests.post(f"http://{self.client.ip_address}:8000/pages/{uuid}", json=profile_data)
            if request.status_code != 200:
                continue
            
            request_data = request.json()

            data_totals = [request_data.get(page, {"total": 0})['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
            insert_profile(uuid, request_data["profile_data"]["profile_name"], request_data["profile_data"]["profile_type"], *data_totals)

