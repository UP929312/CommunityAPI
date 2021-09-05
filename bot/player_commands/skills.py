import discord
from discord.ext import commands

import requests
from bisect import bisect

from utils import error, hf
from emojis import SKILL_EMOJIS
from parse_profile import get_profile_data

SKILLS = ['combat', 'foraging', 'mining', 'farming', 'fishing', 'alchemy', 'enchanting', 'taming', 'carpentry'] # , 'runecrafting'
COUNTED_SKILLS = ['combat', 'foraging', 'mining', 'farming', 'fishing', 'alchemy', 'enchanting', 'taming']

skill_xp_requirements = [0, 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30_000, 50_000, 75_000, 100_000, 200_000, 300_000, 400_000, 500_000, 600_000, 700_000, 800_000, 900_000, 1_000_000, 1_100_000, 1_200_000, 1_300_000, 1_400_000, 1_500_000, 1_600_000, 1_700_000, 1_800_000, 1_900_000, 2_000_000, 2_100_000, 2_200_000, 2_300_000, 2_400_000, 2_500_000, 2_600_000, 2_750_000, 2_900_000, 3_100_000, 3_400_000, 3_700_000, 4_000_000, 4_300_000, 4_600_000, 4_900_000, 5_200_000, 5_500_000, 5_800_000, 6_100_000, 6_400_000, 6_700_000, 7_000_000]
cumulative_xp_reqs = [50,175,375,675,1175,1925,2925,4425,6425,9925,14925,22425,32425,47425,67425,97425,147425,222425,322425,522425,822425,1222425,1722425,2322425,3022425,3822425,4722425,5722425,6822425,8022425,9322425,10722425,12222425,13822425,15522425,17322425,19222425,21222425,23322425,25522425,27822425,30222425,32722425,35322425,38072425,40972425,44072425,47472425,51172425,55172425,59472425,64072425,68972425,74172425,79672425,85472425,91572425,97972425,104972425,111672425] 

#runecrafting_xp_requirements = [50, 150, 160, 2000, 250, 315, 400, 500, 625, 785, 1000, 1250, 1600, 2000, 2465, 3125, 4000, 5000, 6200, 7800, 9800, 12200, 15300]
#runecrafting_cumul_xp_reqs = [0, 50,200,360,2360,2610,2925,3325,3825,4450,5235,6235,7485,9085,11085,13550,16675,20675,25675,31875,39675,49475]

max_levels = {
    "farming": 60,
    "mining": 60,
    "combat": 60,
    "foraging": 50,
    "fishing": 50,
    "enchanting": 60,
    "alchemy": 50,
    "taming": 50,
    "carpentry": 50,
    "runecrafting": 25}

  

def get_level(skill_data, skill):
    return min(bisect(cumulative_xp_reqs, skill_data.get(f'experience_skill_{skill}', 0)), max_levels[skill])

class skills_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['skill'])
    async def skills(self, ctx, username=None, profile=None):
        
        player_data = await get_profile_data(ctx, username, profile)
        if player_data is None:
            return
        username = player_data["username"]

        skill_data = player_data

        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

        total_skill_xp = sum(skill_data.get(f'experience_skill_{skill}', 0) for skill in SKILLS)
        total_counted_levels = sum(get_level(skill_data, skill) for skill in COUNTED_SKILLS)
        skill_average = round(total_counted_levels/len(COUNTED_SKILLS), 2)
        
        embed.add_field(name=f"Skills Data:", value=f"Total Skill XP: **{hf(total_skill_xp)}**\nSkill Average: **{hf(skill_average)}**", inline=False)

        for skill in SKILLS:
            cumulative_xp = int(skill_data.get(f'experience_skill_{skill}', 0))
            current_level = get_level(skill_data, skill)
            if current_level >= max_levels[skill]:
                amount_in = cumulative_xp-cumulative_xp_reqs[max_levels[skill]-1]
                next_level_requirements = 0
                progress = "MAX"
            else:
                amount_in = cumulative_xp-cumulative_xp_reqs[current_level-1]
                next_level_requirements = cumulative_xp_reqs[current_level]-cumulative_xp_reqs[current_level-1]
                progress = f"{round((amount_in/next_level_requirements)*100, 2)}%"

            #print(f"Level {current_level}, NLR: {next_level_requirements}, Amount in: {amount_in}, progress: {progress}")
            embed.add_field(name=f"{SKILL_EMOJIS[skill]} {skill.title()} ({current_level})", value=f"**{hf(amount_in)}**/{hf(next_level_requirements)}\nTotal XP: **{hf(cumulative_xp)}**\nProgress: **{progress}**", inline=True) 

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
