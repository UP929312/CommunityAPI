import discord
from discord.ext import commands

from database_manager import get_max_current_networth, get_max_networth_all_time
from utils import hf
import requests

async def create_emoji(emoji_guild, username):
    image_source = f"https://mc-heads.net/head/{username}"
    image_request = requests.get(image_source)
    emoji = await emoji_guild.create_custom_emoji(name=username, image=image_request.content)
    return emoji


class leaderboard_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["top", "l"])
    async def leaderboard(self, ctx):        
        records = get_max_current_networth()

        embed = discord.Embed(colour=0x3498DB)
        emoji_guild = self.client.get_guild(860247551008440320)

        for i, (uuid, total) in enumerate(records, 1):
            if uuid not in self.client.uuid_conversion_cache:
                self.client.uuid_conversion_cache[uuid] = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]

            username = self.client.uuid_conversion_cache[uuid]
            emoji = discord.utils.find(lambda emoji: emoji.name.lower() == username.lower(), emoji_guild.emojis)
            if emoji is None:
                print("#"*50+f"Creating new emoji for {username}")
                emoji = await create_emoji(emoji_guild, username)
                
            embed.add_field(name=f"{emoji} {username} - #{i}", value=f"Total: **{hf(total)}**", inline=True)

        embed.set_author(icon_url="https://media.discordapp.net/attachments/854829960974565396/868236867944972368/crown.png", name=f"Networth Leaderboard (current)", url="https://discord.com/api/oauth2/authorize?client_id=854722092037701643&permissions=2147601408&scope=bot")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
