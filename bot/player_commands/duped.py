import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests

from utils import error, PROFILE_NAMES, remove_colours, bot_can_send, guild_ids
from parse_profile import get_profile_data
from extract_ids import extract_nbt_dicts, parse_container

class duped_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="duped", aliases=['duped_profile'])
    async def duped_command(self, ctx, provided_username: Optional[str] = None, provided_profile: Optional[str] = None) -> None:
        await self.get_duped(ctx, provided_username, provided_profile, is_response=False)

    @commands.slash_command(name="duped", description="See a list of all player's items that are most likely to be duped.", guild_ids=guild_ids)
    async def duped_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_duped(ctx, username, profile, is_response=True)

    #=========================================================================================================================================
        
    async def get_duped(self, ctx, provided_username: Optional[str] =  None, provided_profile_name: Optional[str] =  None, is_response: bool = False) -> None:

        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        #==================================================================================  
        inv_content = player_data.get("inv_contents", {"data": ""})
        inventory = extract_nbt_dicts(inv_content["data"])
        #'''
        ender_chest = player_data.get("ender_chest_contents", {"data": ""})
        ender_chest = extract_nbt_dicts(ender_chest["data"])

        storage_items = []
        if player_data.get("backpack_contents"):
            for i in range(0, 19):
                page = player_data["backpack_contents"].get(str(i), {"data": ""})
                try:
                    page_data = extract_nbt_dicts(page["data"])
                    storage_items.extend(page_data)
                except TypeError:
                    pass
        #'''
        list_of_items = inventory+ender_chest+storage_items
        filtered_list_of_items = [x for x in list_of_items if x.get("ExtraAttributes", {}).get("uuid", False)]
        list_of_uuids = [x["ExtraAttributes"]["uuid"] for x in filtered_list_of_items]
        ####################################################################################
        
        #pets = [x.get("uuid") for x in player_data.get("pets", []) if x.get("uuid")]
        pets = []
        
        try:
            duped_uuids = requests.post("https://sky.coflnet.com/api/auctions/active/uuid", json=list_of_uuids+pets).json()
        except:
            return await error(ctx, f"Error, Duped API is down!", f"Please wait for it to return, and try again later!", is_response=is_response)
        
        if not duped_uuids:
            embed = discord.Embed(title=f"The player you inputted likely had no duped items.", description="This command works the majority of the time, however isn't 100% accurate, sometimes it can't find duped items.", colour=0x3498DB)
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
            if is_response:
                return await ctx.respond(embed=embed)
            else:
                return await ctx.send(embed=embed)

        #print(duped_uuids)
        list_of_duped_items = []
        for uuid in duped_uuids:
            for item in filtered_list_of_items:
                if not item.get("ExtraAttributes"):
                    if item["uuid"] == uuid:
                        list_of_duped_items.append(item)
                else:
                    if item["ExtraAttributes"]["uuid"] == uuid:
                        list_of_duped_items.append(item)

        desc = "\n".join(remove_colours(x["display"]["Name"]) for x in list_of_duped_items)
        #print(desc)
        
        embed = discord.Embed(title=f"{username}'s list of duped items:", url=f"https://sky.shiiyu.moe/stats/{username}", description=desc, colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        embed.set_thumbnail(url=f"https://cravatar.eu/helmhead/{username}")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)

