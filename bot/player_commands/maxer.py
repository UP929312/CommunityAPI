import discord
from discord.ext import commands
import re

from parse_profile import get_profile_data

from utils import error
from extract_ids import extract_nbt_dicts
from menus import generate_option_picker

NUMBERS = [":one:", ":two:", ":three:", ":four:", ":five:"]#, ":six:", ":seven:", ":eight:", ":nine:"]

gemstone_slots = ['ASPECT_OF_THE_END', 'ASPECT_OF_THE_VOID', 'ZOMBIE_SWORD', 'ORNATE_ZOMBIE_SWORD', 'REAPER_SWORD', 'POOCH_SWORD', 'AXE_OF_THE_SHREDDED', 'YETI_SWORD', 'MIDAS_SWORD', 'DAEDALUS_AXE', 'ASPECT_OF_THE_DRAGON', 'STARRED_BONZO_STAFF', 'BONZO_STAFF', 'BAT_WAND', 'STARRED_STONE_BLADE', 'STONE_BLADE', 'ICE_SPRAY_WAND', 'LIVID_DAGGER', 'STARRED_SHADOW_FURY', 'SHADOW_FURY', 'FLOWER_OF_TRUTH', 'GIANTS_SWORD', 'TITANIUM_DRILL_2', 'TITANIUM_DRILL_3', 'GEMSTONE_DRILL_3', 'BLAZE_ROD', 'MASTIFF_HELMET', 'PERFECT_AMBER_GEM', 'SHARK_SCALE_BOOTS', 'SUPERIOR_DRAGON_BOOTS', 'STARRED_ADAPTIVE_HELMET', 'ADAPTIVE_HELMET', 'STARRED_SHADOW_ASSASSIN_BOOTS', 'SHADOW_ASSASSIN_BOOTS', 'NECROMANCER_LORD_BOOTS', 'SORROW_BOOTS']

class maxer_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['max'])
    async def maxer(self, ctx, username=None):
        
        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        inventory_string = player_data["inv_contents"]["data"]
        inventory_decoded = extract_nbt_dicts(inventory_string)
        inventory_with_lore = [x for x in inventory_decoded if "display" in x and "Lore" in x["display"]]
        
        swords = [x for x in inventory_with_lore if "SWORD" in x["display"]["Lore"][-1]][:5]
        if not swords:
            return await error(ctx, "Error, no swords found", "The bot looked through your inventory and couldn't find any swords, try putting some in!")

        description_list = [f"{NUMBERS[i]} {re.sub('§.', '', x['display']['Name'])}" for i, x in enumerate(swords)]
        
        embed = discord.Embed(title=f"{username}'s Swords", description="\n".join(description_list), url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

        ###########################################################
        option_picked, view_object = await generate_option_picker(ctx, embed, len(swords))
        if option_picked is None:
            return

        item_to_max = swords[option_picked-1]
        ###########################################################
        extras = item_to_max["ExtraAttributes"]
        internal_name = extras["id"]

        
        missing_elements = []

        if not extras.get("rarity_upgrades", False):
            missing_elements.append("Missing a **recombobulator**!")
        hot_potato_books = extras.get("hot_potato_count", 0)
        if hot_potato_books < 15:
            if hot_potato_books < 10:
                missing_elements.append(f"Missing {10-hot_potato_books} **hot** and 5 **fuming** potato books!")
            else:
                missing_elements.append(f"Missing {15-hot_potato_books} **fuming** potato books!")
        if extras.get("modifier", None) != "fabled":
            missing_elements.append(f"Missing the **Fabled** reforge!")
        
        AoW_books = extras.get("art_of_war_count", 0)
        if AoW_books < 5:
            missing_elements.append(f"Missing {5-AoW_books} **Art of War** books!")

            
        if internal_name in ["HYPERION", "ASTRAEA", "SCYLLA", "VALKYRIE"]:
            if not extras.get("ability_scroll", False):
                missing_elements.append(f"Missing an **Necron's Blade Scroll**!")
            if not extras.get("ability_scrolls_value", False):
                missing_elements.append(f"Missing a **Power Scroll!")
                
        if internal_name == "ASPECT_OF_THE_VOID" and extras.get("ethermerge", False):
            missing_elements.append(f"Missing an **Etherwarp Merger and Conduit**!")
        if internal_name == "ASPECT_OF_THE_JERRY" and not extras.get("wood_singularity_count", False):
            missing_elements.append(f"Missing a **Wood Singularity**!")
            
        tuners = extras.get('tuned_transmission', 0)
        if internal_name in ["ASPECT_OF_THE_VOID", "ASPECT_OF_THE_END"] and tuners < 3:
            missing_elements.append(f"Missing {3-tuners} **Transmission Tuners**!")
        ###########################################################
        '''
        Currently included list:
        Recombobulator
        Hot and fuming potato books
        Fabled Reforge
        Art of War books
        Necron Blade scrolls
        Power scrolls
        Etherwarp Merger and Conduit
        Wood singularity
        Transmission Tuners
        '''
        ###########################################################
            

        description = "\n".join(missing_elements) if missing_elements else "The base attributes for this item are already maxed!"

        embed = discord.Embed(title=f"{username}'s Sword", description=description, url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

        '''
        ultimate enchants for swords:
        soul eater 1-5
        ofa
        swarm 1-5
        ultimate wise 1-5 (in case of item with ability)
        chimera 1-5
        combo 1-5
        ultimate jerry 1-5 (in case of aotj)

        in case of hype: wither shield/implosion/shadow warp
        in case of aotj: jerry stone reforge

        '''

        await view_object.message.edit(embed=embed)
  
