import discord  # type: ignore
from discord.ext import commands  # type: ignore

from utils import bot_can_send, guild_ids
from menus import generate_static_preset_menu

data_dict = {
    "networth":    ("[username]",    "Checks the total value of a profile for a user."),
    "auctions":    ("[username]",    "Shows someone's auctions and BINs."),
    "bazaar":      ("<item>",        "Shows the bazaar price for a certain item, e.g. 'cobblestone'."),
    "dungeons":    ("[username]",    "Shows data about someone's dungeon level, including what floors they've beaten."),
    "duped":       ("[username]",    "Shows duped items that a player has on them."),
    "help":        ("<None>",        "Takes you to this command."),
    "invite":      ("<None>",        "Provides instructions on how to invite the bot to your server."),
    "kills":       ("[username]",    "Shows the most mobs a player has killed."),
    "leaderboard": ("[profile_type]","Shows the top 100 players with the highest combined networth!"),
    "link":        ("[ign]",         "Links your in-game name to your discord id so you can leave it out in commands."),
    "lowest_bin":  ("<item>",        "Shows the lowest bin on auction house with that name, use .lb for short!"),
    "maxer":       ("[username]",    "Shows all the attributes and enchantments of the item you select."),
    "minions":     ("[username]",    "Shows the cheapest minions to craft to increase your unique crafted minions count."),
    "missing":     ("[username]",    "Shows the top tier accessories that the player is missing."),
    "price_check": ("<item>",        "Shows historic pricing data about the given item, use .p for short!"),
    "set_prefix":  ("<prefix>",      "Allows an admin to change the prefix of the bot."),
    "skills":      ("[username]",    "Shows a summary of all a users skills, including average."),
    "sky":         ("[username]",    "Links you to someone's sky.shiiyu.moe page, for convenience."),
    "slayer":      ("[username]",    "Shows a summary of someone's slayer data, including how many of each tier someone's killed."),
    "rank":        ("[username]",    "Shows where you place amongst other players with the value of your profile."),
    "weight":      ("[username]",    "Shows a menu of weights which represent how far into the game the player is."),
    "wiki":        ("<item>",        "Shows a page from the Hypixel wiki, to assist in finding a page or item."),
    "weights":     ("[username]",    "Shows someone's senither weight (and overflow weight) in different sections."),
}

categories = {
    "Player Stats Commands": ["dungeons", "kills", "missing", "rank", "skills", "sky", "slayer", "weights"],
    "Price Data Commands":   ["auctions", "bazaar", "lowest_bin", "networth", "price_check"],
    "General Info Commands": ["duped", "leaderboard", "maxer", "minions", "rank", "wiki"],
    "Settings Commands":     ["help", "invite", "link", "set_prefix"],
}

EMOJI_LIST = ["<:stats:915209828983537704>", "<:general_info:915210726900125706>", "<:price_data:915211058728275980>", "<:settings:915211248684134420>"]

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(name="help", aliases=["h", "he", "hel"])
    async def help_command(self, ctx) -> None:
        await self.help(ctx, is_response=False)

    @commands.slash_command(name="help", description="Shows the help command", guild_ids=guild_ids)
    async def help_slash(self, ctx):
        if not bot_can_send(ctx):
            return await ctx.respond("You're not allowed to do that here.", ephemeral=True)
        await self.help(ctx, is_response=True)

    #============================================================================================================================

    async def help(self, ctx, is_response: bool = False) -> None:
        if ctx.guild.id == 1036024217080168488:
            return
        list_of_embeds = []
        for category, commands in categories.items():
            embed = discord.Embed(title=category, colour=0x3498DB)
            for command in commands:
                param, description = data_dict[command]
                param = "" if param == "<None>" else f" {param}"
                embed.add_field(name=f"{command}{param}", value=description, inline=False)            
            
            embed.set_footer(text=f"Command executed by {ctx.author.display_name} | Community Bot. By the community, for the community.")
            list_of_embeds.append(embed)

        await generate_static_preset_menu(ctx=ctx, list_of_embeds=list_of_embeds, emoji_list=EMOJI_LIST, is_response=is_response)
