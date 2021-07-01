import discord
from discord.ext import commands#, tasks
intents = discord.Intents(invites=False, voice_states=False, typing=False, dm_reactions=False, bans=False, emojis=False, integrations=False, webhooks=False,
                          members=False, messages=True, guild_reactions=False, guilds=True, presences=False,)

from utils import load_guild_prefix

print("Importing packages done...")

from networth.networth import networth_cog
from networth.tree import tree_cog
from set_prefix import set_prefix_cog
from help_command import help_cog

print("Importing .py files done...")
    
async def get_prefix(bot, message):
    if message.guild is None:
        return "."
    prefix = load_guild_prefix(message.guild.id)
    #print(f"Prefix = {prefix}, and it's now: {prefix if prefix is not None else '.'}")
    return prefix if prefix is not None else "."

client = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True, owner_id=244543752889303041, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))
#====================================================
@client.event
async def on_ready():
    print("Done")
    print('Bot up and running.')
    print("Loaded in on the community bot!")
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.errors.MissingAnyRole) or isinstance(error, commands.errors.CheckFailure):
        pass
    else:
        raise error

#====================================================

print("Loading cogs...")
all_cogs = [networth_cog, tree_cog, set_prefix_cog, help_cog]
print("Adding cogs...")

for cog in all_cogs:
    client.add_cog(cog(client))
    
print("Cogs all added successfully!")

client.ip_address = "db.superbonecraft.dk"
#client.ip_address = "127.0.0.1"

bot_key = open("bot_key.txt","r").read()
client.run(bot_key)
