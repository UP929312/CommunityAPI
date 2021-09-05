import discord
from discord.ext import commands

import requests
from bisect import bisect

from utils import error, hf, API_KEY
from emojis import SKILL_EMOJIS
from parse_profile import get_profile_data


class guild_print_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def guild_print(self, ctx, skill=None, guild=None):

        print("Starting a guild print")
        if skill.lower() not in ['farming', 'mining', 'combat', 'foraging', 'fishing', 'enchanting', 'alchemy', 'taming', 'carpentry', 'runecrafting']:
            return await error(ctx, "Error, invalid skill!", "This command takes a skill and a guild id to work")

        try:
            response = requests.get(f"https://api.hypixel.net/guild?key={API_KEY}&id={guild}").json()["guild"]
            data = response
            members_uuid = [x['uuid'] for x in data['members']]
            guild_name = response['name']
        except:
            return await error(ctx, "Error, something messed up but I'm not sure what because this command was made very quickly",
                                    "Rushed commands can often lack the normal safety guards a well polished one has.")

        #print(f"Guild name = {guild_name}")
        stuff = []
        for uuid in members_uuid:
            # Get the username
            username = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]
            print(f"Username: {username}, uuid: {uuid}")
            profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
            if not profile_list["profiles"]:
                #print("Skipping", username, uuid)
                continue
            valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]
            profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
            profile = profile["members"][uuid]
            # Extract the right skill
            skill_value = profile.get(f"experience_skill_{skill}", "HIDDEN")
            nice_num = f"{int(skill_value):,}" if skill_value != "HIDDEN" else skill_value
            stuff.append(f"**{username}**: {nice_num}")

        #print(stuff)        
        embed = discord.Embed(title=f"{guild_name}'s current {skill} stats:", description="\n".join(stuff), colour=0x3498DB)

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
