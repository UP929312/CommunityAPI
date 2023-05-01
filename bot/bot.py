import discord  # type: ignore
from discord.ext import commands  # type: ignore

import json  # For loading the uuid conversion cache

from database_manager import load_guild_prefix, load_prefixes, load_linked_accounts
from utils import error as error_embed

intents = discord.Intents(messages=True, guilds=True, emojis=True, message_content=True)

print("1. Importing discord, json and other util packages done.")

from networth.networth import networth_cog
#from networth.guild_networth import guild_networth_cog

print("2. Imported networth and guild networth done.")

from player_commands import *

print("3. Importing all player commands done.")

LOCAL_BOT = True
def get_prefix(bot: commands.Bot, msg: discord.Message):
    if LOCAL_BOT: return "!"
    prefix = bot.prefixes.get(f"{msg.guild.id}", ".") if msg.guild else "."
    return commands.when_mentioned_or(prefix)(bot, msg)

client = commands.AutoShardedBot(command_prefix=get_prefix, help_command=None, case_insensitive=True, owner_id=244543752889303041, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))
client.prefixes = dict(load_prefixes())
client.linked_accounts = dict(load_linked_accounts())

print("4. Client init done and data fetched")

# Load in the stored uuid conversion cache for .leaderboard (they're stored as uuids)
with open("text_files/uuid_conversion_cache.json", 'r') as file:
    client.uuid_conversion_cache = json.load(file)
#====================================================
client.first_run = True

@client.event
async def on_ready() -> None:
    print("on_ready fired! =====")
    if client.first_run:
        client.first_run = False
        print("Done")  # To tell the VM startup was complete
        print('Bot up and running.\nLoaded in on the community bot!')
        client.emoji_guild = await client.fetch_guild(860247551008440320)


@client.event
async def on_command_error(ctx, error) -> None:
    print("In on_command error:", str(error))
    if isinstance(error, (commands.CommandNotFound, commands.errors.MissingAnyRole, discord.Forbidden)):
        pass
    elif isinstance(error, commands.errors.CheckFailure):
        return await ctx.respond("You're not allowed to do that here. Try a bot channel instead?", ephemeral=True)
    else:
        print(f"##### ERROR, The command was: {ctx.message.content}. It was done in {ctx.guild.name}, ({ctx.guild.id}) by {ctx.author.display_name} ({ctx.author.id})")
        print(str(error))
        return await error_embed(ctx, "Error, something failed on our side.", f"The error that occured was: {error}, if this continues, please report it to Skezza#1139,")

@client.event
async def on_interaction(interaction) -> None:
    if interaction.type == discord.InteractionType.application_command:
        message = ", ".join([f"'{argument['name']}: {argument['value']}'" for argument in interaction.data.get('options', {})])
        print(f"-- User {interaction.user.display_name} ({interaction.user.id}) performed `/{interaction.data['name']} {message}`\n"+
              f"-- in {'DMs' if interaction.guild is None else interaction.guild.name} ({'DMs' if interaction.guild is None else interaction.guild.id}) - {'DMs' if interaction.guild is None else interaction.channel.name}")
        await client.process_application_commands(interaction)

@client.event
async def on_application_command_error(ctx, error):
    print(ctx, error)

# For text commands
@client.event
async def on_command_completion(ctx) -> None:
    print(f"-- User {ctx.author.display_name} ({ctx.author.id}) performed `{ctx.message.content}`\n"+
          f"-- in {'DMs' if ctx.guild is None else ctx.guild.name} ({ctx.guild.id if ctx.guild is not None else 'DMs'}) - {'DMs' if ctx.guild is None else ctx.channel.name}")
#====================================================

print("5. Creating cogs list done.")
all_cogs = [networth_cog,]
#all_cogs.append(guild_networth_cog)
all_cogs.extend(player_commands)

for cog in all_cogs:
    client.add_cog(cog(client))

#from test_cog import test_cog
#client.add_cog(test_cog(client))

print("6. Added cogs done.")

#client.ip_address = "149.102.131.110"
client.ip_address = "127.0.0.1"

bot_key = open("text_files/bot_key.txt" if not LOCAL_BOT else "text_files/dev_bot_key.txt","r").read() 
client.run(bot_key)
