import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

import requests
import json

from database_manager import get_max_current_networth
from utils import hf, error

from menus import generate_dynamic_scrolling_menu

#################################
# For the first page (and emojis) only!
async def create_emoji(emoji_guild: discord.Guild, username: str) -> discord.Emoji:
    image_source = f"https://mc-heads.net/head/{username}"
    image_request = requests.get(image_source)
    emoji = await emoji_guild.create_custom_emoji(name=username, image=image_request.content)
    return emoji

async def emoji_page(client: commands.Bot, page: int, username: str, use_emojis: bool=True) -> str:
    if page in [1, 2, 3] and use_emojis:
        emoji_guild = client.get_guild(860247551008440320)
        emoji = discord.utils.find(lambda emoji: emoji.name.lower() == username.lower(), emoji_guild.emojis)
        if emoji is None:
            print("#"*50+f"Creating new emoji for {username}")
            new_emoji: discord.Emoji = await create_emoji(emoji_guild, username)
        emoji_text = f"{emoji or new_emoji}"
    else:
        emoji_text = "<:player_head:876942582444343347>"
        
    return emoji_text
#################################
async def page_generator(ctx: commands.Context, data: list, page: int) -> discord.Embed:
    use_emojis, *data = data  # This is a janky solution
    client: commands.Bot = ctx.bot
    embed: discord.Embed = discord.Embed(colour=0x3498DB)

    cropped_data = data[(page-1)*10:page*10]

    for i, (uuid, total) in enumerate(cropped_data, 1):
        if uuid not in client.uuid_conversion_cache:
            client.uuid_conversion_cache[uuid] = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]

        username = client.uuid_conversion_cache[uuid]
        emoji_text = await emoji_page(client, page, username, use_emojis)

        embed.add_field(name=f"{emoji_text} {username} - #{i+(page-1)*10}", value=f"Total: **{hf(total)}**", inline=True)

    with open("text_files/uuid_conversion_cache.json", 'w') as file:
        json.dump(client.uuid_conversion_cache, file)

    embed.set_author(icon_url="https://media.discordapp.net/attachments/854829960974565396/868236867944972368/crown.png", name=f"Networth Leaderboard (current), page {page}:", url="https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=242666032192&scope=bot%20applications.commands")
    embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

    return embed

class leaderboard_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="leaderboard", aliases=["top", "l"])
    async def leaderboard_command(self, ctx: commands.Context, provided_profile_type: Optional[str] = "regular") -> None:
        await self.get_leaderboard(ctx, provided_profile_type, False)

    @commands.slash_command(name="leaderboard", description="Gets the top Skyblock players", guild_ids=[854749884103917599])
    async def leaderboard_slash(self, ctx, profile_type: Option(str, "profile_type", choices=['regular', 'ironman'], required=False, default="regular")):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_leaderboard(ctx, profile_type, is_response=True)

    #===================================================================================================================================

    async def get_leaderboard(self, ctx: commands.Context, provided_profile_type: Optional[str] = "regular", is_response: bool = False) -> None:
        profile_type = provided_profile_type.lower()
        if profile_type not in ['regular', 'ironman']:
            return await error(ctx, "Error, invalid profile type", "Valid profile types include 'regular' or 'ironman'", is_response=is_response)
        
        records = [(profile_type=="regular")]+get_max_current_networth(profile_type)

        # Menu stuff
        await generate_dynamic_scrolling_menu(ctx=ctx, data=records, page_generator=page_generator, is_response=is_response)
