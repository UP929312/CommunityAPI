import discord
from discord.ext import commands

import requests

from utils import error
from parse_profile import get_profile_data

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

EMOJI_DICT = {
    "farming": "<:farming:832359758404386897>",
    "mining": "<:mining:832359758631272498>",
    "combat": "<:combat:832359758659977226>",
    "foraging": "<:foraging:832359758694187048>",
    "fishing": "<:fishing:832359758635597834>",
    "enchanting": "<:enchanting:832359758329020417>",
    "alchemy": "<:alchemy:832359758236876832>",
    "taming": "<:taming:832360479300648961>",
    "carpentry": "<:carpentry:832359758635597875>",
    "runecrafting": "<:runecrafting:832359758442004551>",
    
    "healer": "<:combat:832359758659977226>",
    "mage": "<:combat:832359758659977226>",
    "berserker": "<:combat:832359758659977226>",
    "archer": "<:combat:832359758659977226>",
    "tank": "<:combat:832359758659977226>",
    
    "revenant": "<:zombie:832251786316349490>",
    "tarantula": "<:spider:832251785820504075>",
    "sven": "<:wolf:832251786059579473>",
    "enderman": "<:enderman:860902315347148801>",
}

PAGE_URLS = {"skills":   ["mining", "foraging", "enchanting", "farming", "combat", "fishing", "alchemy", "taming", "carpentry"],
             "dungeons": ["healer", "mage", "berserker", "archer", "tank"],
             "slayers":  ["revenant", "tarantula", "sven", "enderman"],}

class weights_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['weight', 'w', 'waits'])
    async def weights(self, ctx, username, page):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        response = requests.get(f"https://hypixel-api.senither.com/v1/profiles/{player_data['uuid']}/weight?key={API_KEY}").json()
        if response["status"] != 200:
            return await error(ctx, "Error, the api couldn't fulfill this request.", "As this is an external API, CommunityBot cannot fix this for now. Please try again later.")

        data = response["data"][page]
        total_weight = round(data["weight"]+data["weight_overflow"], 2)

        bank = PAGE_URLS[page]
        if page == "skills":
            description_start = f"Skill average: **{round(data['average_skills'], 2)}**"
        elif page == "dungeons":
            description_start = f"Secrets found: **{data['secrets_found']}**"
        elif page == "slayers":
            description_start = f"Total Coins Spent: **{data['total_coins_spent']}**"

        data = data.get("bosses", None) or data.get("classes", None) or data  # Remap data to be the sub list.

        embed = discord.Embed(title=f"{page.title()} weights for {username}:", description=f"{description_start}\nTotal overall weight: **{round(total_weight, 2)}**",
                              url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)

        for category in bank:
            level = round(data[category]["level"])
            regular = round(data[category]["weight"], 2)
            overflow = round(data[category]["weight_overflow"], 2)
            embed.add_field(name=f"{EMOJI_DICT[category]} {category.title()} ({level})",
                            value=f"Regular: **{regular}**\nOverflow: **{overflow}**\nTotal: **{round(regular+overflow, 2)}**", inline=True)           
    
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
