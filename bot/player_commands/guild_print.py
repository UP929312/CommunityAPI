import discord  # type: ignore
from discord.ext import commands  # type: ignore

import requests
from bisect import bisect

from utils import error, hf, API_KEY
from emojis import SKILL_EMOJIS
from parse_profile import get_profile_data


class guild_print_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="guild_print")
    async def guild_print_command(self, ctx, skill: str=None, guild: str="5d2e5aa477ce8415c3fd00e8") -> None:

        print("Starting a guild print", skill)
        if skill is None or skill.lower() not in ['farming', 'mining', 'combat', 'foraging', 'fishing', 'enchanting', 'alchemy', 'taming', 'carpentry', 'runecrafting', 'catacombs']:
            return await error(ctx, "Error, invalid skill!", "This command takes a skill and a guild id to work")

        try:
            data = requests.get(f"https://api.hypixel.net/guild?key={API_KEY}&id={guild}").json()["guild"]
            members_uuid = [x['uuid'] for x in data['members']]
            guild_name = data['name']
        except:
            return await error(ctx, "Error, something messed up but I'm not sure what because this command was made very quickly",
                                    "Rushed commands can often lack the normal safety guards a well polished one has.")

        #print(f"Guild name = {guild_name}")
        list_of_strings = []
        for uuid in members_uuid:
            # Get the username
            username = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]
            print(f"Username: {username}, uuid: {uuid}")
            profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
            if not profile_list["profiles"]:
                continue
            valid_profiles: list[dict] = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]
            profile_data = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
            profile = profile_data["members"][uuid]
            # Extract the right skill
            if skill != "catacombs":
                skill_value = profile.get(f"experience_skill_{skill}", "HIDDEN")
            else:
                skill_value = profile["dungeons"]["dungeon_types"]["catacombs"].get('experience', 0)
            nice_num = f"{int(skill_value):,}" if skill_value != "HIDDEN" else skill_value
            list_of_strings.append(f"**{username}**: {nice_num}")
     
        embed = discord.Embed(title=f"{guild_name}'s current {skill} stats:", description="\n".join(list_of_strings), colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
