import discord
from discord.ext import commands

import requests
from bisect import bisect

from parse_profile import get_profile_data

from utils import error, format_duration, clean
from emojis import DUNGEON_BOSS_EMOJIS
from menus import generate_static_preset_menu

BOSS_INDEX_DICT = {"1": "Bonzo",
                   "2": "Scarf",
                   "3": "The Professor",
                   "4": "Thorn",
                   "5": "Livid",
                   "6": "Sadan",
                   "7": "Necron"}

emoji_list = ["<:dungeons:864588623394897930>", "<:catacombs:888075448100220949>", "<:master_catacombs:888075454353920010>"]

catacombs_levels = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640 ]

class dungeons_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['d', 'dungeon'])
    async def dungeons(self, ctx, username=None, profile=None):

        player_data = await get_profile_data(ctx, username, profile)
        if player_data is None:
            return
        username = player_data["username"]

        #if not player_data.get("dungeons"):
        #    return await error(ctx, "Error, this person's dungeon API is off!", "This command requires the bot to be able to see their dungeon data to work!")

        ####################################################################################################
        # Page 1: Dungeon skills
        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.add_field(name=f"What to expect?", value=f"Their class skills levels as well as their catacombs level will be here soon! For now, click the buttons to see their floor completions!", inline=False)

        list_of_embeds = [embed, ]
        
        ####################################################################################################
        # Page 2 and 3: Regular and master dungeon levels #master_catacombs vs catacombs
        #level = bisect(catacombs_levels, player_data["dungeons"]["dungeon_types"]["catacombs"]['experience'])
        #Catacombs Level: **{level}**\n
        try:        
            secrets_found = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{player_data['cute_name']}").json()
            secrets_found = secrets_found["dungeons"].get("secrets_found", "???")
        except:
            secrets_found = "???"

        for dungeon_type in ("catacombs", "master_catacombs"):

            dungeon_data = player_data["dungeons"]["dungeon_types"][dungeon_type]

            embed = discord.Embed(title=f"{username}'s {clean(dungeon_type)} Completions", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

            if dungeon_data == {} or "tier_completions" not in dungeon_data:
                if dungeon_type == "catacombs":
                    return await error(ctx, f"Error, this player hasn't played enough of the {clean(dungeon_type)}!", "The player you have looked up hasn't completed any dungeons runs, so their data can't be shown.")
                elif dungeon_type == "master_catacombs":
                    embed.add_field(name=f"This person hasn't done any master floors", value=f"When they complete a floor it'll show up here!", inline=False)
                    list_of_embeds.append(embed)
                    continue

            embed.add_field(name=f"Dungeon Data:", value=f"Secrets Found: **{secrets_found}**", inline=False)

            for floor in list(dungeon_data["tier_completions"]):
                if floor == "0":
                    continue
                completions = int(dungeon_data["tier_completions"][floor])
                
                best_runs = dungeon_data["best_runs"][floor]
                
                best_run = max(best_runs, key=lambda x: x["score_exploration"]+x["score_speed"]+x["score_skill"]+x["score_bonus"])
                best_run_score = best_run["score_exploration"]+best_run["score_speed"]+best_run["score_skill"]+best_run["score_bonus"]
                #
                best_run_time = format_duration(best_run["elapsed_time"], include_millis=False)
                #            
                embed.add_field(name=f"{DUNGEON_BOSS_EMOJIS[floor]} {BOSS_INDEX_DICT[floor]}", value=f"Completions: **{completions}**\nTop Run Score: **{best_run_score}**\nTop Run Time: **{best_run_time}**", inline=True)
            
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
            list_of_embeds.append(embed)
        ####################################################################################################
        # Menu generator
        await generate_static_preset_menu(ctx, list_of_embeds, emoji_list)
