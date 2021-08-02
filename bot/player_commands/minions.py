import discord
from discord.ext import commands

import requests

from utils import error, RARITY_DICT, ITEMS, clean
from parse_profile import get_profile_data

MAX_MINION_LEVELS = {
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
}

NO_ITEM_FOUND = 10000000000

def minion_type(string):
    return "_".join(string.split("_")[:-1])

def minion_level(string):
    return int(string.split("_")[-1])

def get_price(bazaar_dump, item):
    if item.startswith("Upgradable"):
        return NO_ITEM_FOUND
    if ":" in item:
        internal_name, number = item.split(":")
    else:
        internal_name, number = item, 0

    bazaar_item = bazaar_dump.get(internal_name)
    if bazaar_item is None:
        return NO_ITEM_FOUND
    one_item = bazaar_item['buy_summary'][0]['pricePerUnit']
    return one_item*int(number)
    

class minions_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['min', 'minion'])
    async def minions(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        minions = player_data["crafted_generators"]
        if len(minions) == 0:
            return await error(ctx, "Error, this person has never crafted a mininon before!", "Are they the right player?")

        data = requests.get(f"https://api.hypixel.net/skyblock/bazaar").json()["products"]

        unique_minion_types = set([minion_type(x) for x in minions])
        minion_maxes = {}
        for minion in unique_minion_types:
            minions_of_type = [x for x in minions if minion_type(x) == minion]
            max_level_minion = max(minions_of_type, key=lambda x: minion_level(x))
            level = minion_level(max_level_minion)
            if level >= MAX_MINION_LEVELS[minion+"_GENERATOR"]:
                continue
            minion_maxes[minion] = level

        minion_recipes = {}
        for minion, level in minion_maxes.items():
            if level+1 == MAX_MINION_LEVELS[minion+"_GENERATOR"]:
                minion_recipes[minion+f"_{level+1}"] = "Upgradable off the island!"
            else:
                recipe = ITEMS.get(minion+"_GENERATOR_"+str(level), None)
                minion_recipes[minion+f"_{level+1}"] = recipe["recipe"] if recipe else None

        minion_prices = {}
        for minion, recipe in minion_recipes.items():
            if not isinstance(recipe, str):
                minion_prices[minion] = sum([int(get_price(data, x)) for x in recipe if "GENERATOR" not in x])

        ordered = sorted(minion_prices.items(), key=lambda item: item[1])[:12]

        print(ordered)
        #NO_ITEM_FOUND

        embed = discord.Embed(title=f"Cheapest minions to upgrade for {username}", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        
        for i, minion in enumerate(ordered, 1):
            minion_name, price = minion
            embed.add_field(name=f"{clean(minion_name)} - #{i}", value=f"Upgrade cost: ${price}", inline=True)

        await ctx.send(embed=embed)
