import discord
from discord.ext import commands

import requests

from database_manager import get_max_current_networth, insert_profile

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

class regenerate_leaderboard_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.is_owner()
    @commands.command(aliases=["rl"])
    async def regenerate_leaderboard(self, ctx):        
        records = get_max_current_networth()

        for uuid, total in records:
            print(f"Re-calculated {uuid}")
            request = requests.get(f"http://{self.client.ip_address}:8000/pages/{uuid}?api_key={API_KEY}")
            data = [request.json().get(page, {"total": 0})['total'] for page in ("purse", "banking", "inventory", "accessories", "ender_chest", "armor", "vault", "wardrobe", "storage", "pets")]
            insert_profile(uuid, *data)
