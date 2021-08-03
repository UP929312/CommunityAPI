import discord
from discord.ext import commands

import requests

from utils import error, ITEMS, clean, hf, RARITY_DICT
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
    "REDSTONE:": ("ENCHANTED_REDSTONE_BLOCK", 32),
    "MITHRIL:": ("REFINED_MITHRIL", 16),
    "HARD_STONE:": ("ENCHANTED_STONE", 32),
}

EMOJI_DICT = {   
    2:    "<:t2_minion:872063121253097522>",
    3:    "<:t3_minion:872063101837672458>",
    4:    "<:t4_minion:872063093339983932>",
    5:    "<:t5_minion:872063084179619900>",
    6:    "<:t6_minion:872063074683732009>",
    7:    "<:t7_minion:872062768705077288>",
    8:    "<:t8_minion:872063053749948476>",
    9:    "<:t9_minion:872063039879380992>",
    10:   "<:t10_minion:872063029901131826>",
    11:   "<:t11_minion:872063018282917929>",
    12:   "<:t12_minion:872063006639538176>",
}

NO_ITEM_FOUND = 1000000000000
UPGRADABLE = 66666666666

def minion_type(string):
    return "_".join(string.split("_")[:-1])

def minion_tier(string):
    return int(string.split("_")[-1])

def get_price(bazaar_dump, item):
    if item.startswith("Upgradable"):
        return UPGRADABLE
    if ":" in item:
        internal_name, number = item.split(":")
    else:
        internal_name, number = item, 0

    bazaar_item = bazaar_dump.get(internal_name)
    if bazaar_item is None:
        return NO_ITEM_FOUND
    one_item = bazaar_item['buy_summary'][0]['pricePerUnit']
    return int(one_item*int(number))
    

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
            max_tier_minion = max(minions_of_type, key=lambda x: minion_tier(x))
            if minion_tier(max_tier_minion) >= MAX_MINION_TIERS[minion+"_GENERATOR"]:
                continue
            minion_maxes[minion] = minion_tier(max_tier_minion)

        minion_recipes = {}
        for minion, tier in minion_maxes.items():
            minion_id = minion+f"_{tier+1}"
            if tier+1 == MAX_MINION_TIERS[minion+"_GENERATOR"]:
                if (possible_materials := T12_MATERIALS.get(minion)) is None:
                    minion_recipes[minion_id] = UPGRADABLE
                else:  # Calculate minion cost through manual list and bazaar
                    material, count = possible_materials
                    bazaar_item = data[material]
                    price_per = bazaar_item['buy_summary'][0]['pricePerUnit']
                    minion_recipes[minion_id] = int(price_per * count + 2_000_000)
            else:
                recipe = ITEMS.get(minion+"_GENERATOR_"+str(tier), None)
                minion_recipes[minion_id] = recipe["recipe"] if recipe else None

        minion_prices = {}
        for minion, recipe in minion_recipes.items():
            if isinstance(recipe, list):
                #print(minion, recipe)
                minion_prices[minion] = sum([get_price(data, x) for x in recipe if "GENERATOR" not in x])
            else:  # For ints
                minion_prices[minion] = recipe

        ordered = sorted(minion_prices.items(), key=lambda item: item[1])[:12]

        if len(ordered) == 0:
            return await error(ctx, "Error, this person has maxed all minions!", "I guess just wait for the next update?")

        embed = discord.Embed(colour=0x3498DB)
        embed.set_author(name=f"Cheapest minions to upgrade for {username}", icon_url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        
        for i, (minion_name, price) in enumerate(ordered, 1):
            if price // UPGRADABLE:
                price = "Upgradable off the island!"
            elif price // NO_ITEM_FOUND:
                price = "Price unknown"
            else:
                price = f"Upgrade cost: ${hf(price)}"
            embed.add_field(name=f"{EMOJI_DICT[minion_tier(minion_name)]} {clean(minion_name)} - #{i}", value=price, inline=True)

        await ctx.send(embed=embed)
