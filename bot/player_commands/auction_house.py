import discord
from discord.ext import commands

import re
import requests
from datetime import datetime

from utils import error, hf, strfdelta
from parse_profile import get_profile_data

names = ["Expired/Ended auctions", "Buy It Now", "Auctions"]

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

#===================================================================
def get_enchantments(lore):
    list_of_matches = re.finditer(r"((?<=§9)|(?<=§d§l))([A-Za-z]+ )+(X|IX|VIII|VII|VI|V|IV|III|II|I)", lore)

    enchantment_list = [match.group(0) for match in list_of_matches]
    if not enchantment_list: return ""

    enchantment_pairs = [enchantment_list[i:i + 2] for i in range(0, len(enchantment_list), 2)]
    if len(enchantment_pairs[-1]) == 1:
        enchantment_pairs[-1] = (enchantment_pairs[-1][0], "")

    enchantment_string = ""        
    for first, second in enchantment_pairs:
        enchantment_string += f"[{first} {second}]\n"

    formatted_enchants = f'''```ini
[Enchantments]
{enchantment_string}
```
'''
    return formatted_enchants

def to_time(time):
    return datetime.fromtimestamp(time/1000)

#===================================================================

def format_auction(auction):
    title = f"{auction['tier']} {auction['item_name']}"
    expired = to_time(auction["end"]) < datetime.now()
    sell_type = "auction" if "bin" not in auction else "bin"

    bid_count = ""
    time_left = ""

    if 'highest_bid_amount' in auction and auction['highest_bid_amount'] > 0:
        price = hf(auction['highest_bid_amount'])
    else:
        price = hf(auction['starting_bid'])

    if expired and ('highest_bid_amount' in auction and auction['highest_bid_amount'] > auction['starting_bid']):
        status = "SOLD"
    elif expired:
        status = "EXPIRED"
    elif sell_type == "auction":
        status = "BIDDING STAGE"
    else:
        status = "PURCHASABLE"
        
    if not expired:
        time_left = "↳ Time left: "+strfdelta(to_time(auction["end"]) - datetime.now(), '{D}d {H}h {M}m {S:02.0f}s')+"\n"

    if sell_type == "auction":
        bid_count = f"↳ Bids: {len(auction.get('bids', []))}\n"
        price = f"{price} (Currently)"
    else:  # For BINS
        price = f"{price} (Buy it now)"


    list_of_elems = [f"**{title}**\n",
                     f"↳ Status: {status}\n",
                     f"{bid_count}",
                     f"↳ Price: {price}\n",
                     f"{time_left}",]
    
    return_string = "".join(list_of_elems)+get_enchantments(auction['item_lore'])
    return return_string

#===================================================================

class auction_house_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.cooldown(1, 1800, commands.BucketType.user)
    @commands.command(aliases=['ah', 'auctions'])
    async def auction_house(self, ctx, username=None):
      
        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]

        # From here, we have the right profile_id, so we can get all their auction data
        auction_data = requests.get(f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&profile={player_data['profile_id']}").json()
        auctions = auction_data["auctions"]

        expired_auctions = [auction for auction in auctions if to_time(auction["end"]) < datetime.now()]
        bins =             [auction for auction in auctions if to_time(auction["end"]) > datetime.now() and "bin" in auction and auction["bin"]]
        auctions =         [auction for auction in auctions if to_time(auction["end"]) > datetime.now() and "bin" not in auction]

        data = []

        for i, group in enumerate([expired_auctions, bins, auctions]):
            if not group:
                continue
            data.append("**――――――― "+names[i]+" ―――――――**")
            for auction in group:                
                auction = format_auction(auction)
                if sum([len(x) for x in data])+len(auction) > 4000:
                    break
                data.append(auction)

        if not data:
           return await error(ctx, f"{username} doesn't have any active auctions", "If this was you, try heading over to the auction house and putting some things on sale.")
        #=====================
        embed = discord.Embed(title=f"Auction data for {username}", description="\n".join(data) , colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")        
        await ctx.send(embed=embed)
