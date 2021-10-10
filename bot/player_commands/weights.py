import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Optional

import requests

from utils import error, hf, guild_ids
from parse_profile import input_to_uuid
from menus import generate_static_preset_menu

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

EMOJI_DICT = {
    "farming": "<:farming:867330396684943390>",
    "mining": "<:mining:867330462648762368>",
    "combat": "<:combat:867330422018408448>",
    "foraging": "<:foraging:867330412128501770>",
    "fishing": "<:fishing:867330404985339924>",
    "enchanting": "<:enchanting:867330504533606480>",
    "alchemy": "<:alchemy:867330341697355796>",
    "taming": "<:taming:867330484668334084>",
    "carpentry": "<:carpentry:867361518274347039>",
    "runecrafting": "<:runecrafting:867330494679875584>",

    "catacombs": "<:catacombs:864618274900410408>",
    "healer": "<:healer:864611797037350932>",
    "mage": "<:mage:864611797042331699>",
    "berserker": "<:berserker:864611797088075796>",
    "archer": "<:archer:864611797038530590>",
    "tank": "<:tank:864611797033156629>",
    
    "revenant": "<:revenant:867330711191158804>",
    "tarantula": "<:tarantula:867330736368386100>",
    "sven": "<:sven:867330745591529512>",
    "enderman": "<:voidgloom:867330759073464360>",
}
PAGE_URLS = {"dungeons": ["healer", "mage", "berserker", "archer", "tank"],
             "skills":   ["mining", "foraging", "enchanting", "farming", "combat", "fishing", "alchemy", "taming", "carpentry"],
             "slayers":  ["revenant", "tarantula", "sven", "enderman"]
}

EMOJI_LIST = ["<:paper:873158778487443486>", "<:dungeons:864588623394897930>", "<:skills:864588638066311200>",
              "<:slayers:864588648111276072>", "<:misc:854801277489774613>"]

class weights_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="weight", aliases=['weights', 'w', 'waits'])
    async def weight_command(self, ctx, provided_username: Optional[str] = None) -> None:
        await self.get_weights(ctx, provided_username, is_response=False)

    @commands.slash_command(name="weight", description="Gets someone's profile weight", guild_ids=guild_ids)
    async def weight_slash(self, ctx, username: Option(str, "username:", required=False)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_weights(ctx, username, is_response=True)

    @commands.user_command(name="Get profile weight", guild_ids=guild_ids)  
    async def weight_context_menu(self, ctx, member: discord.Member):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_weights(ctx, member.display_name, is_response=True)

    async def get_weights(self, ctx, provided_username: Optional[str] = None, is_response: bool = False):
        player_data: Optional[tuple[str, str]] = await input_to_uuid(ctx, provided_username, is_response=is_response)
        if player_data is None:
            return None
        username, uuid = player_data

        #====================================================================================
        # Main page
        response = requests.get(f"https://hypixel-api.senither.com/v1/profiles/{uuid}/weight?key={API_KEY}").json()
        if response["status"] != 200:
            return await error(ctx, "Error, the api couldn't fufill this request.", "As this is an external API, CommunityBot cannot fix this for now. Please try again later.", is_response=is_response)
        response = response["data"]
    
        total_regular_weight = round(response["weight"], 2)
        total_overflow_weight = round(response["weight_overflow"], 2)

        list_of_elems = [f"Total Regular Weight: **{total_regular_weight}**",
                         f"Total Overflow Weight: **{total_overflow_weight}**",
                         f"Total Weight: **{round(total_regular_weight+total_overflow_weight, 2)}**",
                          "",
                          "Click the buttons to start!",
                          "<:dungeons:864588623394897930> Dungeons",
                          "<:skills:864588638066311200> Skills",
                          "<:slayers:864588648111276072> Slayer",
                          "<:misc:854801277489774613> Info"]
        
        embed = discord.Embed(title=f"Weights Calculator For {username}:", description="\n".join(list_of_elems),
                              url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)

        list_of_embeds = [embed]
        #====================================================================================
        # Skills, slayer and dungeons
        for page in ["dungeons", "skills", "slayers"]:
            data = response[page]
            if data is None:
                embed = discord.Embed(title=f"{page.title()} weights for {username}:", description=f"There doesn't seem to be anything here?\nThis is most likely because {username} hasn't done any dungeons before.",
                                      url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
                embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
                embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
                list_of_embeds.append(embed)
                continue

            if page == "skills":
                description_start = f"Skill average: **{round(data['average_skills'], 2)}**"
            elif page == "slayers":
                description_start = f"Total coins spent: **{hf(data['total_coins_spent'])}**"
            elif page == "dungeons":
                description_start = f"Secrets found: **{data['secrets_found']}**"

            embed = discord.Embed(title=f"{page.title()} weights for {username}:", description=f"Total {page.removesuffix('s')} weight: **{round(data['weight']+data['weight_overflow'], 2)}**\n{description_start}",
                                  url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)

            if page == "dungeons":
                catacombs_weight = round(data['types']['catacombs']['weight'], 2)
                catacombs_overflow = round(data['types']['catacombs']['weight_overflow'], 2)
                embed.add_field(name=f"{EMOJI_DICT['catacombs']} Cata ({int(data['types']['catacombs']['level'])})",
                                value=f"Regular: **{catacombs_weight}**\nOverflow: **{catacombs_overflow}**\nTotal: **{round(catacombs_weight+catacombs_overflow, 2)}**", inline=True)

            remapped_data = data.get("bosses", None) or data.get("classes", None) or data  # Remap data to be the sub list.

            for category in PAGE_URLS[page]:
                level = int(remapped_data[category]["level"])
                regular = round(remapped_data[category]["weight"], 2)
                overflow = round(remapped_data[category]["weight_overflow"], 2)
                embed.add_field(name=f"{EMOJI_DICT[category]} {category.title()} ({level})",
                                value=f"Regular: **{regular}**\nOverflow: **{overflow}**\nTotal: **{round(regular+overflow, 2)}**", inline=True)
                
            list_of_embeds.append(embed)
        #====================================================================================
        # Info page
        embed = discord.Embed(title=f"Info page", description=f"Weights are a concept that attempts to represent how far into the game you are, whether that be in slayer, dungeons, or your skills. It uses an extensive formula to calculate the weights. The formula and the data, however, is provided by the Senither API [found here](https://hypixel-api.senither.com/), so no changes can be made to it.\n\nFor a rough idea of how it's calculated, each skills/slayer/dungeon level has a specific number that decides how important to classify that level, and any level above max level will get diminishing returns.", colour=0x3498DB)
        list_of_embeds.append(embed)
        #====================================================================================
        for i, embed in enumerate(list_of_embeds):
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
            list_of_embeds[i] = embed
        
        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, is_response=is_response)

