import discord
from discord.ext import commands

import requests
from bisect import bisect

from utils import error, hf
from parse_profile import get_profile_data

#=====================
slayer_level_requirements = {
    'zombie': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
    'spider': [5, 25, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
    'wolf':   [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000],
    'enderman': [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000],
}

SLAYER_COST = [2_000, 7_500, 20_000, 50_000, 100_000]  # Same for all of them

MOB_EMOJI_DICT = {"zombie": "<:zombie:832251786316349490>",
                  "spider": "<:spider:832251785820504075>",
                  "wolf": "<:wolf:832251786059579473>",
                  "enderman": "<:enderman:860902315347148801>",}
BOSSES = list(MOB_EMOJI_DICT.keys())  # For doing [:3]

#=====================
def get_mob_data(mob, slayer_bosses):
    xp = slayer_bosses.get(mob).get('xp', 0)
    level = bisect(slayer_level_requirements[mob], xp)
    next_level_xp = 0 if level >= len(slayer_level_requirements)-1 else slayer_level_requirements[mob][min(level, 8)]
    progress = "MAX" if level >= len(slayer_level_requirements)-1 else f"{round((xp/next_level_xp)*100, 2)}%"
    return level, xp, next_level_xp, progress

def add_mob_table(mob, slayer_bosses):
    return "```scala\n"+"\n".join(f"Tier {x+1}: "+str(slayer_bosses[mob].get(f"boss_kills_tier_{x}", 0)) for x in range(5))+"```"
#=====================
class slayer_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        
    @commands.command()
    async def slayer(self, ctx, username=None):
      
        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        slayer_bosses = player_data["slayer_bosses"]
        #=====================
        total_slayer_xp = sum(slayer_bosses.get(mob).get('xp', 0) for mob in BOSSES)
        #=====================
        total_paid = 0
        for i in range(5):
            for mob in BOSSES:
                total_paid += SLAYER_COST[i]*slayer_bosses.get(mob).get(f"boss_kills_tier_{i}", 0)
        #=====================
        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        #=====================
        embed.add_field(name="Slayer Data", value=f"Total Slayer XP: **{hf(total_slayer_xp)}**\nSlayer Coins Spent: **{hf(total_paid)}**", inline=False)
        #=====================
        for mob in BOSSES[:3]:
            current_level, current_xp, next_level_xp, progress = get_mob_data(mob, slayer_bosses)
            embed.add_field(name=f"{MOB_EMOJI_DICT[mob]} {mob.title()} ({current_level})", value=f"**{hf(current_xp)}**/{hf(next_level_xp)}\nTotal XP: (**{hf(current_xp)}**)\nProgress: **{progress}**", inline=True)

        for mob in BOSSES[:3]:
            string = add_mob_table(mob, slayer_bosses)
            embed.add_field(name="Boss Kills:", value=string, inline=True)

        # Because endermen make this annoying
        current_level, current_xp, next_level_xp, progress = get_mob_data('enderman', slayer_bosses)
        embed.add_field(name=f"{MOB_EMOJI_DICT['enderman']} Enderman ({current_level})", value=f"**{hf(current_xp)}**/{hf(next_level_xp)}\nTotal XP: (**{hf(current_xp)}**)\nProgress: **{progress}**", inline=True)

        embed.insert_field_at(index=8, name='\u200b', value='\u200b', inline=True)
        embed.insert_field_at(index=9, name='\u200b', value='\u200b', inline=True)

        string = add_mob_table('enderman', slayer_bosses)
        embed.add_field(name="Boss Kills:", value=string, inline=True)

        embed.insert_field_at(index=11, name='\u200b', value='\u200b', inline=True)
        embed.insert_field_at(index=12, name='\u200b', value='\u200b', inline=True)        
        #=====================
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
