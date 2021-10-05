import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.app import Option  # type: ignore
from typing import Iterator, Optional, Union

import re
import requests
from datetime import datetime

from utils import error, hf, format_duration, PROFILE_NAMES
from emojis import ITEM_RARITY
from parse_profile import get_profile_data




names = ["Expired/Ended auctions", "Buy It Now", "Auctions"]

with open('text_files/hypixel_api_key.txt') as file:
    API_KEY = file.read()

#===================================================================
def get_enchantments(lore: str) -> str:
    list_of_matches: Iterator = re.finditer(r"((?<=§9)|(?<=§d§l))([A-Za-z]+ )+(X|IX|VIII|VII|VI|V|IV|III|II|I)", lore)

    enchantment_list = [match.group(0) for match in list_of_matches]
    if not enchantment_list: return ""
    sorted_list = sorted(enchantment_list, key=lambda ench: ench.startswith("Ultimate"), reverse=True)

    enchantment_pairs: list = [sorted_list[i:i + 2] for i in range(0, len(sorted_list), 2)]
    if len(enchantment_pairs[-1]) == 1:
        enchantment_pairs[-1] = (enchantment_pairs[-1][0], "")

    enchantment_string: str = "\n".join([f"[{first.replace('_', ' ')}, {second.replace('_', ' ')}]".replace(", ]", "]") for first, second in enchantment_pairs])

    formatted_enchants: str = f'''```ini
[Enchantments]
{enchantment_string}
```
'''
    return formatted_enchants

def to_time(time: int) -> datetime:
    return datetime.fromtimestamp(time/1000)

#===================================================================

def format_auction(auction: dict) -> str:
    title = f"{ITEM_RARITY[auction['tier']]} {auction['item_name']}"
    expired = to_time(auction["end"]) < datetime.now()
    sell_type = "auction" if "bin" not in auction else "bin"

    bid_count = ""
    time_left = ""

    price = hf(auction.get("highest_bid_amount", 0) or auction.get("starting_bid", 0))

    if expired and ('highest_bid_amount' in auction and auction['highest_bid_amount'] >= auction['starting_bid']):
        status = "SOLD"
    elif expired:
        status = "EXPIRED"
    elif sell_type == "auction":
        status = "BIDDING STAGE"
    else:
        status = "PURCHASABLE"

    if auction["claimed"] and len(auction["claimed_bidders"]) < len(set([x["bidder"] for x in auction["bids"]])):
        return ""
        
    if not expired:
        time_left = "↳ Time left: "+format_duration(to_time(auction["end"]) - datetime.now())+"\n"

    if sell_type == "auction":
        bid_count = f"↳ Bids: {len(auction.get('bids', []))}\n"
        price = f"{price} ({'Currently' if not expired else 'Final Price'})"
    else:  # For BINS
        price = f"{price} {'(Buy it now)' if not expired else ''}"


    list_of_elems = [
        f"**{title}**\n",
        f"↳ Status: {status}\n",
        f"{bid_count}",
        f"↳ Price: {price}\n",
        f"{time_left}",]
    
    return_string: str = "".join(list_of_elems)+get_enchantments(auction['item_lore'])
    return return_string

#===================================================================

class auction_house_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.client = bot

    @commands.command(name="auction_house", aliases=['ah', 'auctions'])
    async def auction_house_command(self, ctx: commands.Context, provided_username: Optional[str] =  None, provided_profile_name: Optional[str] = None) -> None:
        await self.get_auction_house(ctx, provided_username, provided_profile_name, is_response=False)

    @commands.slash_command(name="auctions", description="Gets auctions data about someone", guild_ids=[854749884103917599])
    async def auction_house_slash(self, ctx, username: Option(str, "username:", required=False),
                             profile: Option(str, "profile", choices=PROFILE_NAMES, required=False)):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_auction_house(ctx, username, profile, is_response=True)

    @commands.user_command(name="Get auction data", guild_ids = [854749884103917599])  
    async def auction_house_context_menu(self, ctx, member: discord.Member):
        if not (ctx.channel.permissions_for(ctx.guild.me)).send_messages:
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.get_auction_house(ctx, member.display_name, None, is_response=True)

    #=========================================================================================================================================
        
    async def get_auction_house(self, ctx: commands.Context, provided_username: Optional[str] =  None, provided_profile_name: Optional[str] =  None, is_response: bool = False) -> None:
          
        player_data: Optional[dict] = await get_profile_data(ctx, provided_username, provided_profile_name, is_response=is_response)
        if player_data is None:
            return
        username = player_data["username"]

        # From here, we have the right profile_id, so we can get all their auction data
        auction_data = requests.get(f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&profile={player_data['profile_id']}").json()
        auctions: list[dict] = auction_data["auctions"]

        expired_auctions = [auction for auction in auctions if to_time(auction["end"]) < datetime.now()]
        bins =             [auction for auction in auctions if to_time(auction["end"]) > datetime.now() and "bin" in auction and auction["bin"]]
        active_auctions =  [auction for auction in auctions if to_time(auction["end"]) > datetime.now() and "bin" not in auction]

        data = []

        for group_name, group in zip(names, [expired_auctions, bins, active_auctions]):
            if not group:
                continue
            data.append(f"**――――――― {group_name} ―――――――**")
            for auction in group:                
                auction_string = format_auction(auction)
                if auction_string == "":
                    continue
                if sum([len(x) for x in data])+len(auction_string) > 4000:
                    break
                data.append(auction_string)
            if data[-1] == f"**――――――― {group_name} ―――――――**":
                data = data[:-1]

        if not data:
           return await error(ctx, f"{username} doesn't have any active auctions", "If this was you, try heading over to the auction house and putting some things on sale.", is_response=is_response)
        #=====================
        embed = discord.Embed(title=f"Auction data for {username}", description="\n".join(data) , colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        if is_response:
            await ctx.respond(embed=embed)
        else:
            await ctx.send(embed=embed)
