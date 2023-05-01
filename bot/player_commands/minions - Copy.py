import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests

from utils import error, ITEMS, clean, hf, API_KEY, PROFILE_NAMES, bot_can_send, guild_ids
from emojis import MINION_TIER_EMOJIS
from parse_profile import get_profile_data

MAX_MINION_TIERS = {
    "ACACIA_GENERATOR": 11,
    "BIRCH_GENERATOR": 11,
    "BLAZE_GENERATOR": 11,
    "CACTUS_GENERATOR": 12,
    "CARROT_GENERATOR": 12,
    "CAVESPIDER_GENERATOR": 11,
    "CHICKEN_GENERATOR": 12,
    "CLAY_GENERATOR": 11,
    "COAL_GENERATOR": 12,
    "COBBLESTONE_GENERATOR": 12,
    "COCOA_GENERATOR": 12,
    "COW_GENERATOR": 12,
    "CREEPER_GENERATOR": 11,
    "DARK_OAK_GENERATOR": 11,
    "DIAMOND_GENERATOR": 12,
    "EMERALD_GENERATOR": 12,
    "ENDER_STONE_GENERATOR": 11,
    "ENDERMAN_GENERATOR": 11,
    "FISHING_GENERATOR": 11,
    "FLOWER_GENERATOR": 11,
    "GHAST_GENERATOR": 11,
    "GLOWSTONE_GENERATOR": 11,
    "GOLD_GENERATOR": 12,
    "GRAVEL_GENERATOR": 11,
    "ICE_GENERATOR": 11,
    "IRON_GENERATOR": 12,
    "JUNGLE_GENERATOR": 11,
    "LAPIS_GENERATOR": 12,
    "MAGMA_CUBE_GENERATOR": 11,
    "MELON_GENERATOR": 12,
    "MITHRIL_GENERATOR": 12,
    "MUSHROOM_GENERATOR": 12,
    "NETHER_WARTS_GENERATOR": 12,
    "OAK_GENERATOR": 11,
    "OBSIDIAN_GENERATOR": 12,
    "PIG_GENERATOR": 12,
    "POTATO_GENERATOR": 12,
    "PUMPKIN_GENERATOR": 12,
    "QUARTZ_GENERATOR": 11,
    "RABBIT_GENERATOR": 12,
    "REDSTONE_GENERATOR": 12,
    "REVENANT_GENERATOR": 12,
    "SAND_GENERATOR": 11,
    "SHEEP_GENERATOR": 12,
    "SKELETON_GENERATOR": 11,
    "SLIME_GENERATOR": 11,
    "SNOW_GENERATOR": 11,
    "SPIDER_GENERATOR": 11,
    "SPRUCE_GENERATOR": 11,
    "SUGAR_CANE_GENERATOR": 12,
    "TARANTULA_GENERATOR": 11,
    "VOIDLING_GENERATOR": 11,
    "WHEAT_GENERATOR": 12,
    "ZOMBIE_GENERATOR": 11,
    "HARD_STONE_GENERATOR": 11,
    "MYCELIUM_GENERATOR": 12,
    "RED_SAND_GENERATOR": 12,
    "INFERNO_GENERATOR": 12,
}

T12_MATERIALS = {
    "COBBLESTONE": ("ENCHANTED_COBBLESTONE", 1024),
    "OBSIDIAN": ("ENCHANTED_OBSIDIAN", 1024),
    "COAL": ("ENCHANTED_COAL_BLOCK", 16),
    "IRON": ("ENCHANTED_IRON_BLOCK", 16),
    "GOLD": ("ENCHANTED_GOLD_BLOCK", 16),
    "DIAMOND": ("ENCHANTED_DIAMOND_BLOCK", 16),
    "LAPIS": ("ENCHANTED_LAPIS_LAZULI_BLOCK", 64),
    "EMERALD": ("ENCHANTED_EMERALD_BLOCK", 16),
    "REDSTONE": ("ENCHANTED_REDSTONE_BLOCK", 32),
    "MITHRIL": ("REFINED_MITHRIL", 16),
    "HARD_STONE": ("ENCHANTED_HARD_STONE", 32),
    "REVENANT": ("REVENANT_VISCERA", 64),
    "RED_SAND_GENERATOR": ("ENCHANTED_RED_SAND_CUBE", 32),
}


NO_ITEM_FOUND = 1000000000000
UPGRADABLE = 66666666666

def minion_type(string: str) -> str:
    return "_".join(string.split("_")[:-1])

def minion_tier(string: str) -> int:
    return int(string.split("_")[-1])

def get_price(bazaar_dump: dict, item: str) -> int:
    internal_name, number = (item.split(":")) if ":" in item else (item, 0)  # Get quantity off the end = STONE:3 = 3x Stone

    for i in range(9):
        internal_name = internal_name.removesuffix(f"-{i}")  # Removes "-3" from LOG-3 so it can be found at bazaar

    if (bazaar_item := bazaar_dump.get(internal_name)) is None:
        print(internal_name)
        return NO_ITEM_FOUND
    one_item = bazaar_item['buy_summary'][0]['pricePerUnit']
    return one_item*int(number)
    

class minions_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="minions", aliases=['min', 'minion'])
    async def minions_command(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None) -> None:
        await self.minions(ctx, provided_username, provided_profile_name, is_response=False)

    @commands.slash_command(name="minions", description="Gets a players cheapest minions to upgrade", guild_ids=guild_ids)
    async def minions_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.minions(ctx, username, profile, is_response=True)
    
    #===================================================================================================================================
        
    async def minions(self, ctx, provided_username: Optional[str] = None, provided_profile_name: Optional[str] = None, is_response: bool = False) -> None:

        ########## One: Get the right profile and username
        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        
        username = player_data["username"]
        ########## Two: Get all the minions from each player on that profile
        combined_data = requests.get(f"https://api.hypixel.net/skyblock/profile?key={API_KEY}&profile={player_data['profile_id']}").json()
        # Get a list of all the different players on the profile
        all_crafted_generators = [combined_data["profile"]["members"][member].get("crafted_generators", []) for member in combined_data["profile"]["members"]]
        # Get the crafted_generators for each member in the profile
        minions = [item for sublist in all_crafted_generators for item in sublist]  # Combine all the lists
            
        if len(minions) == 0:
            return await error(ctx, "Error, this person has never crafted a mininon before!", "Are they the right player?", is_response=is_response)

        ########## Three: Get the bazaar data + override 4 common minions
        data = requests.get(f"https://api.hypixel.net/skyblock/bazaar").json()["products"]
        data["YELLOW_FLOWER"] =       {'buy_summary': [{'pricePerUnit': 35}, None]} # Hard code dandelion from builder
        data["ENCHANTED_DANDELION"] = {'buy_summary': [{'pricePerUnit': 160*35}, None]}
        data["MELON_BLOCK"] =         {'buy_summary': [{'pricePerUnit': 9*data["MELON"]["buy_summary"][0]["pricePerUnit"]}, None]}
        data["SILVER_FANG"] =         {'buy_summary': [{'pricePerUnit': 125*data["GHAST_TEAR"]["buy_summary"][0]["pricePerUnit"]}, None]}
        
        ########## Four: Get all the minion sets, e.g. {"SNOW": 4, "COBBLESTONE": 3}
        unique_minion_types = set([minion_type(x) for x in minions])
        minion_maxes = {}
        for minion in unique_minion_types:
            minions_of_type = [x for x in minions if minion_type(x) == minion]
            max_tier_minion = max(minions_of_type, key=lambda x: minion_tier(x))
            if minion_tier(max_tier_minion) >= MAX_MINION_TIERS[minion+"_GENERATOR"]:
                continue
            minion_maxes[minion] = minion_tier(max_tier_minion)
    
        ########## Five: Get the prices for each of the next tier up
        minion_prices = {}
        for minion, tier in minion_maxes.items():
            minion_id = minion+f"_{tier+1}"
            # If it's being upgraded to max tier
            if tier+1 == MAX_MINION_TIERS[minion+"_GENERATOR"]:
                
                if (possible_materials := T12_MATERIALS.get(minion)) is None:
                    # If it's not a mining T12 minion, e.g. farming (Chicken T12)
                    minion_prices[minion_id] = UPGRADABLE
                else:  # Calculate minion cost through manual list and bazaar
                    material, count = possible_materials
                    bazaar_item = data[material]
                    price_per = bazaar_item['buy_summary'][0]['pricePerUnit']
                    minion_prices[minion_id] = price_per * count+2_000_000
            else:  # If not, just get the recipe from Moulberry's
                recipe = ITEMS.get(f"{minion}_GENERATOR_{tier+1}", {"recipe": NO_ITEM_FOUND})["recipe"]
                minion_prices[minion_id] = sum([get_price(data, x) for x in recipe if "GENERATOR" not in x])

        ordered = sorted(minion_prices.items(), key=lambda item: item[1])[:12]

        if len(ordered) == 0:
            return await error(ctx, "Error, this person has maxed all minions!", "I guess just wait for the next update?", is_response=is_response)

        ########## Six: Present in the embed
        embed = discord.Embed(colour=0x3498DB)
        embed.set_author(name=f"Cheapest minions to upgrade for {username}", icon_url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        
        for i, (minion_name, price) in enumerate(ordered, 1):
            if price % UPGRADABLE == 0:
                price_formatted = "Upgradable with [Terry](https://hypixel-skyblock.fandom.com/wiki/Terry%27s_Shop)!"
            elif price % NO_ITEM_FOUND == 0:
                price_formatted = "Price unknown"
            else:
                price_formatted = f"Upgrade cost: {hf(int(price))}"
            embed.add_field(name=f"{MINION_TIER_EMOJIS[minion_tier(minion_name)]} {clean(minion_name)} - #{i}", value=price_formatted, inline=True)

        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
