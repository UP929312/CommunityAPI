import discord
from discord.ext import commands

from database_manager import get_specific_networth_data, get_all_networth_data, get_sum_networth_data
from emojis import PAGE_ICON_EMOJIS
from parse_profile import get_profile_data
from utils import error


def get_percent_categories(uuid, user_data):
    """
    Returns the percentage that the uuid's group is less than, 100% = 0 money, 0.03% = Extremely rich
    """
    data = get_all_networth_data()

    categories = {}
    for i, category in enumerate(["purse", "banking", "inventory", "accessories", "ender chest", "armor", "vault", "wardrobe", "storage", "pets"]):
        # Get all purses from data, but only if they're less than the user's purse, then banking
        if user_data[i] < 1:
            continue
        filtered = [x[i] for x in data if x[i] < user_data[i]]
        categories[category] = ((len(filtered)+1)/len(data))*100
    return categories

def overall_percent(uuid, user_data):
    """
    Returns the percentage that the total networth is less than
    """
    user_total = sum(user_data)
    data = get_sum_networth_data()
    filtered = [x[0] for x in data if x[0] < user_total]
    return ((len(filtered)+1)/len(data))*100

def fix(number):
    number = round(100-number[1], 3)
    return max(number, 0.01)


class rank_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def rank(self, ctx, username=None):

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]
        uuid = player_data['uuid']

        user_data = get_specific_networth_data(uuid)
        if len(user_data) == 0:
            return await error(ctx, "Error, not enough data!", "We don't know how much your profile is worth right now, please use the networth command first!")
        
        categories = get_percent_categories(uuid, user_data[0])
        sorted_data = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_data) < 4:
            return await error(ctx, "Error, not enough data!", "This person's API settings are to restrictive, or they have lots of empty containers.")

        total_networth_percentage = None, overall_percent(uuid, user_data[0])

        string = [f"{PAGE_ICON_EMOJIS['overall']} Their overall networth is in the highest {fix(total_networth_percentage)}% of players.",
                  f"",
                  f"{PAGE_ICON_EMOJIS[sorted_data[0][0]]} For {sorted_data[0][0]}, they're in the top {fix(sorted_data[0])}% of players.",
                  f"{PAGE_ICON_EMOJIS[sorted_data[1][0]]} For {sorted_data[1][0]}, they're in the top {fix(sorted_data[1])}% of players.",
                  f"{PAGE_ICON_EMOJIS[sorted_data[2][0]]} For {sorted_data[2][0]}, they're in the top {fix(sorted_data[2])}% of players.",
                  f"",
                  f"{PAGE_ICON_EMOJIS[sorted_data[-1][0]]} For {sorted_data[-1][0]}, they're in the bottom {fix(sorted_data[-1])}% of players."]

        embed = discord.Embed(title=f"{username}'s stats:", description="\n".join(string), url=f"https://sky.shiiyu.moe/stats/{username}", colour=0x3498DB)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{username}")
        
        embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        await ctx.send(embed=embed)