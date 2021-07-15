import discord
from discord.ext import commands

import requests
from difflib import SequenceMatcher

from utils import *

items = []

print("Importing SlothPixel's item list for bazaar")
#'''
try:
    item_dict = requests.get("https://api.slothpixel.me/api/skyblock/items").json()

    for item in item_dict:
        items.append((item, item_dict[item]["name"].replace(" ", "_").upper()))
        #items = [(item, item_dict[item]["name"].replace(" ", "_").upper()) for item in item_dict]
except:
    pass
#'''

print("Imported item list complete.")

def get_item_by_internal_name(internal_id):
    for key, value in item_dict.items():
        if key == internal_id:
            return value["name"]
    return None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class bazaar_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=['b', 'ba', 'baz'])
    async def bazaar(self, ctx, *, user_input=None):
        # If the api is down?
        if not items:
            return await error(ctx, "This command is currently non-functional!", "The api this command is using is currently down for maintenance, please wait for it to come back!")
        elif user_input is None:
            return await error(ctx, "No item given.", "Please give the item you want to check the price of at the bazaar.")

        user_input = user_input.lower()
        if user_input.startswith("e "):
            user_input = "enchanted"+user_input[1:]
        
        closest_internal_name_list = [(similar(user_input.replace(" ", "_"), item.lower()), item) for item, display_name in items]
        closest_internal_name = max(closest_internal_name_list, key=lambda x: x[0])
        closest_display_name_list  = [(similar(user_input, display_name.lower()), item) for item, display_name in items]   
        closest_display_name  = max(closest_display_name_list, key=lambda x: x[0])

        similarity, internal_name = max([closest_internal_name, closest_display_name], key=lambda x: x[0])

        if similarity < 0.6:
            return await error(ctx, "No item with that name found at the bazaar.", "Is the item availible to purchase at the bazaar?")    
            
        response_object = requests.get(f'https://api.slothpixel.me/api/skyblock/bazaar/{internal_name}').json()
        if "error" in response_object:
            return await error(ctx, "An error occured", "This might be because you typed the name in wrong, or an API issue.")

        list_of_strings = [f"Buy it instantly price: ${int(response_object['buy_summary'][0]['pricePerUnit'])}",
                           f"Sell it instantly price: ${int(response_object['sell_summary'][0]['pricePerUnit'])}",
                           f"Buy volume: {response_object['quick_status']['buyVolume']}",
                           f"Sell volume: {response_object['quick_status']['sellVolume']}"]

        embed = discord.Embed(title=f"Bazaar pricing information for {get_item_by_internal_name(internal_name) or internal_name}", description="\n".join(list_of_strings), url=f"https://bazaartracker.com/product/{internal_name.lower()}", colour=0x3498DB)
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)
