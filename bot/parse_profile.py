import requests
#import re

from utils import error

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

ALLOWED_CHARS = {"_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}

async def input_to_uuid(ctx, username):
    """
    This returns a dictionary of all the player's profile data.
    It will take a already given username, but if one isn't given, it will
    first check if they've linked their account, if not, it will try
    parsing their ign from their discord nicks, by trimming off their tag,
    e.g. '[Admin] Notch' will get parsed as 'Notch'.
    """
    nick = None  # Used to detect if we fell back on parsing nick
    if username is None:  # If no username is given
        linked_account = ctx.bot.linked_accounts.get(f"{ctx.author.id}", None)
        if linked_account:  # Check if they've linked their account
            username = linked_account
        else:  # If not, parse their nickname
            nick = ctx.author.display_name
            username = nick.split("]")[1] if "]" in nick else nick
            username = "".join([char for char in username if char.lower() in ALLOWED_CHARS])
            
    uuid_request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if uuid_request.status_code > 200:
        return await error(ctx, "Error! Username was incorrect.", "Make sure you spelled the target player's name correctly.")

    # When we can't find a username, request.text will be '', if we can, it'll be the json string
    if not uuid_request.text:
        if not nick:
            return await error(ctx, "Error! Username was incorrect.", "Make sure you spelled the target player's name correctly.")
        else:
            return await error(ctx, "Error, could not parse username from discord nickname.", "No linked account was found through link_account, and no username was given. Please link your account or provide a username")
        
    uuid = uuid_request.json()["id"]
    return username, uuid

async def get_profile_data(ctx, username):
    # Convert username/linked_account/nick to uuid
    data = await input_to_uuid(ctx, username)
    if data is None:
        return None
    username, uuid = data
    #################################
    # Fetch profile from hypixel's API with uuid

    profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()

    if profile_list == {'success': False, 'cause': 'Invalid API key'}:
        print("############################### Error, key has failed again!")
        return await error(ctx, "Error, the api key used to run this bot has failed.", "This may be because Hypixel removed the key. A fix is coming soon!")

    # profiles can be None, or not exist as key
    if profile_list.get('profiles') is None:  # If we can't find any profiles, they never made one
        return await error(ctx, "That user has never joined Skyblock before!", "Make sure you typed the name correctly and try again.")

    valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]

    if not valid_profiles:
        return await error(ctx, "Error, cannot find profiles for this user!", "Make sure you spelled the target player's name correctly")
    
    profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])
    #################################
    # Save the profile data and some other bits because they're handy

    profile_dict = profile["members"][uuid]

    profile_dict["uuid"] = uuid
    profile_dict["username"] = username
    profile_dict["profile_id"] = profile["profile_id"]
    profile_dict["cute_name"] = profile["cute_name"]

    return profile_dict

