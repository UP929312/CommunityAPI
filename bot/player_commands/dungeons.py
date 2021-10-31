import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests
from bisect import bisect

from parse_profile import get_profile_data

from utils import error, format_duration, clean, hf, PROFILE_NAMES, guild_ids
from emojis import DUNGEON_BOSS_EMOJIS
from menus import generate_static_preset_menu

BOSS_INDEX_DICT = {"1": "Bonzo",
                   "2": "Scarf",
                   "3": "The Professor",
                   "4": "Thorn",
                   "5": "Livid",
                   "6": "Sadan",
                   "7": "Necron"}

CLASS_EMOJIS = {"catacombs": "<:catacombs:864618274900410408>",
                "healer": "<:healer:864611797037350932>",
                "mage": "<:mage:864611797042331699>",
                "berserk": "<:berserker:864611797088075796>",
                "archer": "<:archer:864611797038530590>",
                "tank": "<:tank:864611797033156629>",
}
CLASSES = list(CLASS_EMOJIS.keys())[1:]

EMOJI_LIST = ["<:dungeons:864588623394897930>", "<:catacombs:888075448100220949>", "<:master_catacombs:888075454353920010>"]

LEVEL_REQS = [50, 125, 235, 395, 625, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 35640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640, 30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640, 285559640, 360559640, 453559640, 569809640, 1000000000000000000000000000000]

   
class dungeons_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(name="dungeons", aliases=['d', 'dungeon'])
    async def dungeons_command(self, ctx, provided_username: Optional[str] = None, provided_profile: Optional[str] = None) -> None:
        await self.get_dungeons(ctx, provided_username, provided_profile, is_response=False)

    @commands.slash_command(name="dungeons", description="Gets dungeons data about someone", guild_ids=guild_ids)
    async def dungeons_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_dungeons(ctx, username, profile, is_response=True)

    @commands.user_command(name="Get dungeons data", guild_ids=guild_ids)  
    async def dungeons_context_menu(self, ctx, member: discord.Member):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_dungeons(ctx, member.display_name, None, is_response=True)

    #======================================================================================================================================

    async def get_dungeons(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None, is_response: bool = False) -> None:
        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        #if not player_data.get("dungeons"):
        #    return await error(ctx, "Error, this person's dungeon API is off!", "This command requires the bot to be able to see their dungeon data to work!", is_response=is_response)

        try:        
            secrets_found = requests.get(f"https://sky.shiiyu.moe/api/v2/dungeons/{username}/{player_data['cute_name']}").json()
            secrets_found = secrets_found["dungeons"].get("secrets_found", "???")
        except:
            secrets_found = "???"

        ####################################################################################################
        # Page 1: Dungeon skills
        embed = discord.Embed(title=f"{username}", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.add_field(name=f"Dungeon Data:", value=f"Secrets Found: **{secrets_found}**", inline=False)
        
        catacombs_xp = player_data["dungeons"]["dungeon_types"]["catacombs"].get('experience', 0)
        xps = {"catacombs": catacombs_xp}

        for class_type in CLASSES:
            xps[class_type] = player_data["dungeons"]["player_classes"][class_type].get("experience", 0)

        for class_name, xp in xps.items():
            level = bisect(LEVEL_REQS, xp)
            if level == 50:
                progress = f"**{hf(xp-LEVEL_REQS[49])}**/0"
                progress_percent = "**MAXED**"
            else:
                progress = f"**{hf(xp-LEVEL_REQS[level-1])}**/{hf(LEVEL_REQS[level]-LEVEL_REQS[level-1])}"
                progress_raw = (xp-LEVEL_REQS[level-1])/(LEVEL_REQS[level]-LEVEL_REQS[level-1])
                progress_percent = "**"+str(round(progress_raw*100, 2))+"%**"
                
            embed.add_field(name=f"{CLASS_EMOJIS[class_name]} {class_name.title()} - ({level})", value=f"{progress}\nTotal XP: (**{hf(xp)}**)\nProgress: {progress_percent}", inline=True)
        
        list_of_embeds = [embed]
        
        ####################################################################################################
        # Page 2 and 3: Regular and master dungeon levels #master_catacombs vs catacombs
        for dungeon_type in ("catacombs", "master_catacombs"):

            dungeon_data = player_data["dungeons"]["dungeon_types"][dungeon_type]

            display = "M" if dungeon_type == "master_catacombs" else "F"

            embed = discord.Embed(title=f"{username}'s {clean(dungeon_type)} Completions", url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
            embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")

            if dungeon_data == {} or "tier_completions" not in dungeon_data:
                if dungeon_type == "catacombs":
                    return await error(ctx, f"Error, this player hasn't played enough of the dungeons!", "The player you have looked up hasn't completed any dungeons runs, so their data can't be shown.", is_response=is_response)
                elif dungeon_type == "master_catacombs":
                    embed.add_field(name=f"This person hasn't done any master floors", value=f"When they complete a floor it'll show up here!", inline=False)
                    list_of_embeds.append(embed)
                    continue

            embed.add_field(name=f"Dungeon Data:", value=f"Secrets Found: **{secrets_found}**", inline=False)

            for floor in sorted(list(dungeon_data["tier_completions"])):
                if floor == "0":
                    continue
                
                completions = int(dungeon_data["tier_completions"][floor])

                best_runs = dungeon_data["best_runs"][floor]

                if dungeon_type == "catacombs":
                    best_run = max(best_runs, key=lambda x: x["score_exploration"]+x["score_speed"]+x["score_skill"]+x["score_bonus"])
                    best_run_score = best_run["score_exploration"]+best_run["score_speed"]+best_run["score_skill"]+best_run["score_bonus"]
                    row_1 = f"Top Run Score: **{best_run_score}**"
                else:
                    s_runs = [x for x in best_runs if (x["score_exploration"]+x["score_speed"]+x["score_skill"]+x["score_bonus"]) >= 270]
                    if not s_runs:
                        row_1 = f"S PB: **None**"
                    else:
                        fastest_s_run = min(s_runs, key=lambda x: x["elapsed_time"])
                        row_1 = f"S PB: **{format_duration(fastest_s_run['elapsed_time'])}**"

                s_plus_runs = [x for x in best_runs if (x["score_exploration"]+x["score_speed"]+x["score_skill"]+x["score_bonus"]) >= 300]
                if not s_plus_runs:
                    s_plus_row = f"S+ PB: **None**"
                else:
                    fastest_s_plus_run = min(s_plus_runs, key=lambda x: x["elapsed_time"])
                    s_plus_row = f"S+ PB: **{format_duration(fastest_s_plus_run['elapsed_time'])}**"
        
                embed.add_field(name=f"{DUNGEON_BOSS_EMOJIS[floor]} {BOSS_INDEX_DICT[floor]} ({display}{floor})", value=f"Completions: **{completions}**\n{row_1}\n{s_plus_row}", inline=True)
            
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
            list_of_embeds.append(embed)
        ####################################################################################################
        # Menu generator
        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, is_response=is_response)
