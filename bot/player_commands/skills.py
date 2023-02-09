import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests
from bisect import bisect

from utils import error, hf, PROFILE_NAMES, bot_can_send, guild_ids, autocomplete_display_name
from emojis import SKILL_EMOJIS
from parse_profile import get_profile_data

SKILLS = ['combat', 'foraging', 'mining', 'farming', 'fishing', 'alchemy', 'enchanting', 'taming', 'carpentry']
CUMULATIVE_XP_REQS = [50,175,375,675,1175,1925,2925,4425,6425,9925,14925,22425,32425,47425,67425,97425,147425,222425,322425,522425,822425,1222425,1722425,2322425,3022425,3822425,4722425,5722425,6822425,8022425,9322425,10722425,12222425,13822425,15522425,17322425,19222425,21222425,23322425,25522425,27822425,30222425,32722425,35322425,38072425,40972425,44072425,47472425,51172425,55172425,59472425,64072425,68972425,74172425,79672425,85472425,91572425,97972425,104972425,111672425] 

##runecrafting_xp_requirements = [50, 150, 160, 2000, 250, 315, 400, 500, 625, 785, 1000, 1250, 1600, 2000, 2465, 3125, 4000, 5000, 6200, 7800, 9800, 12200, 15300]
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
    "runecrafting": 25,
}

level_squares = ["⬛", "⬜", "🟩", "🟦", "🟪", "🟨", "<:pink_square:1073051068998623342>", "🟦", "🟥", "[🔴]"]

def get_level(skill_data: dict, skill: str) -> int:
    return min(bisect(CUMULATIVE_XP_REQS, skill_data.get(f'experience_skill_{skill}', 0)), max_levels[skill])

class skills_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="skills", aliases=['skill'])
    async def skills_command(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None) -> None:
        await self.skills(ctx, provided_username, provided_profile_name, is_response=False)
    
    @commands.slash_command(name="skills", description="Gets a players skills", guild_ids=guild_ids)
    async def skills_slash(self, ctx, username: Option(str, "username:", required=False, autocomplete=discord.utils.basic_autocomplete(values=["red", "green", "blue"])),
                                       profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.skills(ctx, username, profile, is_response=True)

    async def skills(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None, is_response: bool = False) -> None:
        
        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        skill_data = player_data

        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

        total_skill_xp = sum(skill_data.get(f'experience_skill_{skill}', 0) for skill in SKILLS)
        total_counted_levels = sum(get_level(skill_data, skill) for skill in SKILLS)
        skill_average = round(total_counted_levels/len(SKILLS), 2)

        skyblock_level = int(skill_data["leveling"]["experience"])//100
        skyblock_level_overflow = int(skill_data["leveling"]["experience"]) % 100
        
        embed.add_field(name=f"Skills Data:", value=f"Total Skill XP: **{hf(total_skill_xp)}**\nSkill Average: **{hf(skill_average)}**", inline=True)
        embed.add_field(name=f"Skyblock Level:", value=f"Level {skyblock_level} - {level_squares[skyblock_level//40]}\n[{skyblock_level_overflow}/100]", inline=True)
        embed.add_field(name=f"\u200b", value="\u200b", inline=True)

        for skill in SKILLS:
            cumulative_xp = int(skill_data.get(f'experience_skill_{skill}', 0))
            current_level = get_level(skill_data, skill)
            if current_level >= max_levels[skill]:
                amount_in = cumulative_xp-CUMULATIVE_XP_REQS[max_levels[skill]-1]
                next_level_requirements = 0
                progress = "MAX"
            else:
                amount_in = cumulative_xp-CUMULATIVE_XP_REQS[current_level-1]
                next_level_requirements = CUMULATIVE_XP_REQS[current_level]-CUMULATIVE_XP_REQS[current_level-1]
                progress = f"{round((amount_in/next_level_requirements)*100, 2)}%"

            #print(f"Level {current_level}, Next Level Reqs: {next_level_requirements}, Amount in: {amount_in}, progress: {progress}")
            embed.add_field(name=f"{SKILL_EMOJIS[skill]} {skill.title()} ({current_level})", value=f"**{hf(amount_in)}**/{hf(next_level_requirements)}\nTotal XP: **{hf(cumulative_xp)}**\nProgress: **{progress}**", inline=True) 

        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
