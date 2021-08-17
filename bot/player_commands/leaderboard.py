import discord
from discord.ext import commands

import requests
import json

from database_manager import get_max_current_networth, get_max_networth_all_time
from utils import hf

from menus import generate_dynamic_scrolling_menu

#################################
# For the first page (and emojis) only!
async def create_emoji(emoji_guild, username):
    image_source = f"https://mc-heads.net/head/{username}"
    image_request = requests.get(image_source)
    emoji = await emoji_guild.create_custom_emoji(name=username, image=image_request.content)
    return emoji

async def emoji_page(client, page, username):
    if page == 1:
        emoji_guild = client.get_guild(860247551008440320)
        emoji = discord.utils.find(lambda emoji: emoji.name.lower() == username.lower(), emoji_guild.emojis)
        if emoji is None:
            print("#"*50+f"Creating new emoji for {username}")
            emoji = await create_emoji(emoji_guild, username)
        emoji_text = f"{emoji}"
    else:
        emoji_text = "<:player_head:876942582444343347>"
        
    return emoji_text
#################################
async def page_generator(ctx, data, page):
    client = ctx.bot
    embed = discord.Embed(colour=0x3498DB)

    cropped_data = data[(page-1)*10:page*10]

    for i, (uuid, total) in enumerate(cropped_data, 1):
        if uuid not in client.uuid_conversion_cache:
            client.uuid_conversion_cache[uuid] = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]

        username = client.uuid_conversion_cache[uuid]
        emoji_text = await emoji_page(client, page, username)

        embed.add_field(name=f"{emoji_text} {username} - #{i+(page-1)*10}", value=f"Total: **{hf(total)}**", inline=True)

    with open("text_files/uuid_conversion_cache.json", 'w') as file:
        json.dump(client.uuid_conversion_cache, file)

    embed.set_author(icon_url="https://media.discordapp.net/attachments/854829960974565396/868236867944972368/crown.png", name=f"Networth Leaderboard (current), page {page}:", url="https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=242666032192&scope=bot%20applications.commands")
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

    return embed

class leaderboard_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["top", "l"])
    async def leaderboard(self, ctx):        
        records = get_max_current_networth()

        # Menu stuff
        await generate_dynamic_scrolling_menu(ctx=ctx, data=records, page_generator=page_generator)
        
        
