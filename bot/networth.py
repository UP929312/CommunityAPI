import discord
from discord.ext import commands

import requests

from utils import error
from utils import human_number as hf
from generate_description import do_description, generate_pet_description

page_names = ["main", "inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"]

##########
ip = "http://db.superbonecraft.dk:8000"
ip = "127.0.0.1"
#########

class networth_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["nw", "n", "net", "worth"])
    async def networth(self, ctx, username=None, page="main"):

        if username is None:
            nick = ctx.author.nick
            username = nick.split("]")[1] if "]" in nick else nick

        if page.lower() not in page_names:
            return await ctx.send("Invalid page, please pick from:", ", ".join(page_names))

        request = requests.get(f"http://127.0.0.1:8000/pages/{username}")
        if request.status_code != 200:
            if request.status_code >= 500:  # Over 500 = Server fails
                return await error(ctx, "Error, an exception has occured", "This happened internally. If it's continues, let the lead dev know (Skezza#1139)")
            if request.status_code != 400:  # !400 = Meh
                return await error(ctx, "Error, no connection", "The bot couldn't connect to the API, it may be down or failing")
            # 400 = Username not found
            return await error("ctx", "Error, that person could not be found", "Perhaps you input the incorrect name?")

        data = request.json()
        total = data[page]["total"]
        top_x = data[page]["prices"]

        embed = discord.Embed(title=f"{username}'s {page.replace('_', ' ').title()} Networth {hf(float(total))}", colour=0x3498DB)


        '''
        {'total': 542169215, 'value': {'base_price': 3500000, 'price_source': 'BIN', 'held_item': {'value': 34000000, 'price_source': 'BIN'}, 'pet_skin': {'value': 499000000, 'price_source': 'BIN'}, 'pet_level_bonus': {'amount': '28346078 xp', 'worth': 5669215}},
        'item': {'uuid': None, 'type': 'SHEEP', 'exp': 28346078.6142195, 'active': False, 'tier': 'LEGENDARY', 'heldItem': 'MINOS_RELIC', 'candyUsed': 0, 'skin': 'SHEEP_BLACK'}}
        '''

        if page == "main":
            pass
        else:
            for price_object in top_x:
                item = price_object["item"]
                if page == "pets":
                    value = generate_pet_description(price_object["value"])
                    embed.add_field(name=f"Level {price_object['value']['pet_level']} {item['type'].replace('_', ' ').title()} ➜ {hf(price_object['total'])}", value=value, inline=False)
                else:
                    value = do_description(price_object["value"])
                    embed.add_field(name=f"{item['name']} ➜ {hf(price_object['total'])}", value=value, inline=False)

        embed.set_thumbnail(url=f"https://cravatar.eu/helmhead/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")    
        return await ctx.send(embed=embed)

