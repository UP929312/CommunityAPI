import discord  # type: ignore
from discord.ext import commands  # type: ignore
from datetime import datetime
import requests
from typing import Optional

from utils import error, API_KEY, ITEMS, guild_ids
from parse_profile import get_profile_data
from menus import generate_option_picker
from emojis import NUMBER_EMOJIS

# If you want to change these, change the "if tree" values as well...
category_names = ["Forge Completions", "Auction Bids", "Auction Endings"]
EMOJI_OPTIONS = ["<:reforge:854750152048246824>", "<:winning_bid:856491169750712320>", "<:auctions:917037274057814048>"]
BACK_EMOJI = ":arrow_backward:"

FORGE_TIMES = {
    'REFINED_DIAMOND': 28800,
    'REFINED_MITHRIL': 21600,
    'REFINED_TITANIUM': 43200,
    'FUEL_TANK': 36000,
    'BEJEWELED_HANDLE': 1800,
    'DRILL_ENGINE': 108000,
    'GOLDEN_PLATE': 21600,
    'MITHRIL_PLATE': 64800,
    'GEMSTONE_MIXTURE': 14400,
    'PERFECT_JASPER_GEM': 72000,
    'PERFECT_RUBY_GEM': 72000,
    'PERFECT_JADE_GEM': 72000,
    'PERFECT_SAPPHIRE_GEM': 72000,
    'PERFECT_AMBER_GEM': 72000,
    'PERFECT_TOPAZ_GEM': 72000,
    'PERFECT_AMETHYST_GEM': 72000,
    'MITHRIL_PICKAXE': 2700,
    'BEACON_2': 72000,
    'TITANIUM_TALISMAN': 50400,
    'DIAMONITE': 21600,
    'POWER_CRYSTAL': 7200,
    'FORGE_TRAVEL_SCROLL': 18000,
    'REFINED_MITHRIL_PICKAXE': 7920,
    'MITHRIL_DRILL_1': 14400,
    'MITHRIL_FUEL_TANK': 36000,
    'MITHRIL_DRILL_ENGINE': 54000,
    'BEACON_3': 108000,
    'TITANIUM_RING': 72000,
    'PURE_MITHRIL': 43200,
    'ROCK_GEMSTONE': 79200,
    'PETRIFIED_STARFALL': 50400,
    'GOBLIN_OMELETTE_PESTO': 72000,
    'AMMONITE;4': 1036800,
    'GEMSTONE_DRILL_1': 3600,
    'CRYSTAL_HOLLOWS_TRAVEL_SCROLL': 36000,
    'MITHRIL_DRILL_2': 30,
    'TITANIUM_DRILL_ENGINE': 108000,
    'GOBLIN_OMELETTE': 64800,
    'BEACON_4': 144000,
    'TITANIUM_ARTIFACT': 129600,
    'HOT_STUFF': 86400,
    'GOBLIN_OMELETTE_SUNNY_SIDE': 72000,
    'GEMSTONE_DRILL_2': 30,
    'TITANIUM_DRILL_1': 230400,
    'TITANIUM_DRILL_2': 30,
    'TITANIUM_DRILL_3': 30,
    'TITANIUM_FUEL_TANK': 90000,
    'BEACON_5': 180000,
    'TITANIUM_RELIC': 259200,
    'GOBLIN_OMELETTE_SPICY': 72000,
    'GEMSTONE_DRILL_3': 30,
    'RUBY_POLISHED_DRILL_ENGINE': 72000,
    'GEMSTONE_FUEL_TANK': 108000,
    'GOBLIN_OMELETTE_BLUE_CHEESE': 72000,
    'TITANIUM_DRILL_4': 30,
    'GEMSTONE_DRILL_4': 30,
    'SAPPHIRE_POLISHED_DRILL_ENGINE': 108000,
    'AMBER_MATERIAL': 25200,
    'DIVAN_HELMET': 82800,
    'DIVAN_CHESTPLATE': 82800,
    'DIVAN_LEGGINGS': 82800,
    'DIVAN_BOOTS': 82800,
    'AMBER_POLISHED_DRILL_ENGINE': 180000,
    'PERFECTLY_CUT_FUEL_TANK': 180000,
    'DIVAN_DRILL': 216000,
}

class notify_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="notify", aliases=['notifyme', 'forge_notify'])
    async def notify_command(self, ctx) -> None:
        await self.notify(ctx, is_response=False)

    @commands.slash_command(name="notify", description="Notifies the player about auctions or forge completions", guild_ids=guild_ids)
    async def notify_slash(self, ctx):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.notify(ctx, is_response=True)

    async def notify(self, ctx, is_response: bool = False) -> None:
        
        username = "Skezza"
        player_data: Optional[dict] = await get_profile_data(ctx, username, None, is_response=is_response)
        if player_data is None:
            return

        embed = discord.Embed(title=f"What kind of notification would you like to add or remove?", description=f"\> Forge Completions\n\> Auction Bids\n\> Auction Endings", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        value, view = await generate_option_picker(ctx, embed, EMOJI_OPTIONS)
        category = category_names[EMOJI_OPTIONS.index(str(value))]  # Index the emoji and get the proper name

        # If you want to change these, change the list values as well...
        if category == "Forge Completions":
            incomplete_tasks = []
            forge_tasks = player_data["forge"]["forge_processes"]["forge_1"].values()
            if not forge_tasks:
                print("Nothing in forge")
                embed = discord.Embed(title=f"You have nothing in your forge!", description=f"Try putting some items on there, an re-running the command.", colour=0x3498DB)
            else:
                quick_forge_bonus = player_data["mining_core"]["nodes"]["forge_time"]*0.005
                formatted_tasks = [{"internal_name": x["id"], "start_time": x["startTime"], "slot": x["slot"]} for x in forge_tasks]

                list_of_strings = []                
                counter = 1
                for slot in range(1, 5):
                    potential_item = [x for x in formatted_tasks if x["slot"] == slot]
                    if not any(potential_item):
                        string = f"**Empty Slot - Slot {item['slot']}**\nOpen to new crafts"
                    else:
                        item = potential_item[0]
                        duration = FORGE_TIMES[item['internal_name']]-(FORGE_TIMES[item['internal_name']]*quick_forge_bonus)
                        end_time = int((item['start_time']+duration)/1000)
                        extra = "Completed" if end_time < datetime.now().timestamp() else f"{NUMBER_EMOJIS[counter]} Finishes"
                        if end_time > datetime.now().timestamp():
                            incomplete_tasks.append(item)
                            counter += 1
                        string = f"**{ITEMS[item['internal_name']]['name']} - Slot {item['slot']}**\n{extra} at <t:{end_time}>"
                    list_of_strings.append(string)
    
                if not any(["Finishes" in x for x in list_of_strings]):
                    print("All casts are complete")
                    embed = discord.Embed(title=f"All your forge casts are complete!", description=f"Go grab them to clear up some space!", colour=0x3498DB)
                else:
                    embed = discord.Embed(title=f"Which forge slot would you like to modify or remove?", description="\n".join(list_of_strings), colour=0x3498DB)

            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")

            # We now have a new view, it'll either have options or just a back button
            options = [NUMBER_EMOJIS[x["slot"]] for x in incomplete_tasks]+[BACK_EMOJI]
            print(options)
            value, view = await generate_option_picker(ctx, embed, options, is_response=is_response, message_object=view.message)
            if value == BACK_EMOJI:
                self.notify(ctx, is_response)
            else:
                item = incomplete_tasks[NUMBER_EMOJIS.index(value)]
                print("Item:", item)
                print("Slot:", value)
            

        elif category in ["Auction Bids", "Auction Endings"]:
            #request = requests.get(f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&uuid={player_data['uuid']}")
            #auctions = 5
            pass


        '''
        # Everything is fine, send it
        embed = discord.Embed(title=f"Category: {category}", description=f"Description", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
        '''
        '''
{"forge_1":{
"4":{"type":"ITEM_CASTING","id":"POWER_CRYSTAL","startTime":1641403542166,"slot":4,"notified":false}


{type:"subPlayers",data:"uuid1,uuid2,uuid3,..."} 
and then receive full auctions on every action? {type,"bidNotify",data:{auctionobject}
{type,"sellNotify",data:{auctionobject}

'''
