import discord
from discord.ext import commands

from database_manager import get_saved_profiles
from parse_profile import get_profile_data
from utils import error, hf

#import matplotlib.pyplot as plt
#import pandas as pd
import io

class graph_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["g", "plot"])
    async def graph(self, ctx, username=None):
        return

        player_data = await get_profile_data(ctx, username)
        if player_data is None:
            return
        username = player_data["username"]
        uuid = player_data["uuid"]

        records = get_saved_profiles(uuid)
        if len(records) < 5:
            return await error(ctx, "Error, this player doesn't have enough data", "For this command to work, there must be enough data to show, try running the command a few times later for it to properly show change!")

        # PLOTTNG THE GRAPH

        filled_data = records
        #print(filled_data[0][0])

        time = [x[0] for x in filled_data]
        values = [sum(x[1:]) for x in filled_data]
        

        with plt.style.context('dark_background'):
            # Set outside the data colour
            plt.rcParams['figure.facecolor'] = '131316'
            df = pd.DataFrame({"Total networth value": values, 'Time': time})
            ax = df.plot(kind='line', x='Time', y='Total networth value', rot=0, color="#3498DB")

        # Set colour behind the data
        ax.set_facecolor("#292B2F")
        ax.set_xticklabels(labels=[x.strftime("%d/%m") for x in time], rotation=45, rotation_mode="anchor", ha="right")
        ax.set_yticklabels(labels=[hf(y) for y in values])

        # --------
        if len(ax.xaxis.get_ticklabels()) > 10:
            for index, label in enumerate(ax.xaxis.get_ticklabels()):
                if index % 7 != 0:
                    label.set_visible(False)
        # LABELS
        plt.ylabel('Total networth value')
        plt.title("Value of networth over time")
        # -------
        # BUFFER + SHOWING
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
            
        await ctx.send(file=discord.File(buf, filename=f"graph.png"))


        #embed = discord.Embed(title=f"Networth history for {username}", description=f"\n".join([", ".join(str(x) for x in records)]), colour=0x3498DB)
        #embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
        #await ctx.send(embed=embed)
