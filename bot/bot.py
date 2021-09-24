import discord
from discord.ext import commands

import json  # For loading the uuid conversion cache

intents = discord.Intents(guild_reactions=False, members=False, invites=False, voice_states=False, typing=False, dm_reactions=False, bans=False, presences=False, integrations=False, webhooks=False,
                          messages=True, guilds=True, emojis=True)

from database_manager import load_guild_prefix, load_prefixes, load_linked_accounts
from utils import safe_delete, safe_send, error as error_embed

print("Importing packages done...")

from networth.networth import networth_cog
from networth.guild_networth import guild_networth_cog

print("Imported all non-player_commands")

from player_commands import *

print("Importing .py files done...")

linked_accounts = dict(load_linked_accounts())
prefixes = dict(load_prefixes())

'''
def get_prefix(bot, msg):
    prefix = bot.prefixes.get(f"{msg.guild.id}", ".") if msg.guild else "."
    return commands.when_mentioned_or(prefix)(bot, msg)
#'''
#'''
def get_prefix(bot, msg):
    return "!"
#'''
client = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True, owner_id=244543752889303041, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))
client.prefixes = prefixes
client.linked_accounts = linked_accounts

# Load in the stored uuid conversion cache for .leaderboard (they're stored as uuids)
with open("text_files/uuid_conversion_cache.json", 'r') as file:
    client.uuid_conversion_cache = json.load(file)
#====================================================
@client.event
async def on_ready():
    print("Done")
    print('Bot up and running.')
    print("Loaded in on the community bot!")
        
@client.event
async def on_command_error(ctx, error):
    if any([isinstance(error, x) for x in {commands.CommandNotFound, commands.errors.MissingAnyRole,
                                           commands.errors.CheckFailure, discord.errors.Forbidden}
          ]):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        # ALLOW PEOPLE WITH MANAGE MESSAGES TO BYPASS THE COOLDOWN
        if ctx.guild is not None and ctx.author.guild_permissions.manage_messages: 
            await ctx.reinvoke()
        else:
            await safe_delete(ctx.message)
            await safe_send(ctx.author, error)
    else:
        print(f"##### ERROR, The command was: {ctx.message.content}. It was done in {ctx.guild.name}, ({ctx.guild.id}) by {ctx.author.display_name} ({ctx.author.id})")
        print(str(error))
        return await error_embed(ctx, "Error, something failed on our side.", f"The error that occured was: {error}, if this continues, please report it to Skezza#1139,")

@client.event
async def on_command_completion(ctx):
    print(f"-- User {ctx.author.display_name} ({ctx.author.id}) performed `{ctx.message.content}`\n"+
          f"-- in {'DMs' if ctx.guild is None else ctx.guild.name} ({ctx.guild.id if ctx.guild is not None else 'DMs'}) - {'DMs' if ctx.guild is None else ctx.channel.name}")

#====================================================

print("Loading cogs...")
all_cogs = [guild_networth_cog,]
all_cogs.append(networth_cog)
all_cogs.extend(player_commands)
print("Adding cogs...")

for cog in all_cogs:
    client.add_cog(cog(client))
    
print("Cogs all added successfully!")

client.ip_address = "db.superbonecraft.dk"
#client.ip_address = "127.0.0.1"

bot_key = open("text_files/bot_key.txt","r").read()
client.run(bot_key)
