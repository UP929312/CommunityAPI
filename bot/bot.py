import discord
from discord.ext import commands#, tasks
intents = discord.Intents(invites=False, voice_states=False, typing=False, dm_reactions=False, bans=False, emojis=False, integrations=False, webhooks=False,
                          members=False, messages=True, guild_reactions=False, guilds=False, presences=False,)

intents = discord.Intents.default()
print("Importing packages done...")

from networth.networth import networth_cog
from networth.tree import tree_cog

print("Importing .py files done...")

client = commands.Bot(command_prefix = ["."], help_command=None, case_insensitive=True, owner_id=244543752889303041, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))
#====================================================
@client.event
async def on_ready():
    print("Done")
    print('Bot up and running.')
    print("Loaded in on the community bot!")
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        '''
        try:
            await ctx.send("Command not recognised!", delete_after=30.0)
        except discord.errors.Forbidden:
            pass
        '''
        pass
    # This caused issues with CarlBot
    elif isinstance(error, commands.NotOwner):
        await ctx.author.send("The is a developer command and cannot be used by you.")
    else:
        raise error 
#====================================================

print("Loading cogs...")
all_cogs = [networth_cog, tree_cog]
print("Adding cogs...")

for cog in all_cogs:
    client.add_cog(cog(client))
    
print("Cogs all added successfully!")

bot_key = open("bot_key.txt","r").read()
client.run(bot_key)
