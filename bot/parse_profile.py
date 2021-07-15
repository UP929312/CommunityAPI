import requests

from utils import error

with open("text_files/hypixel_api_key.txt") as file:
    API_KEY = file.read()

ALLOWED_CHARS = {"_", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}


async def get_profile_data(ctx, username):
    """
    This returns a dictionary of all the player's profile data.
    It will take a already given username, but if one isn't given, it will
    first check if they've linked their account, if not, it will try
    parsing their ign from their discord nicks, by trimming off their tag,
    e.g. '[Admin] Notch' will get parsed as 'Notch'.
    """
    if username is None:
        linked_account = ctx.bot.linked_accounts.get(f"{ctx.author.id}", None)
        if linked_account:
            username = linked_account
        if not linked_account:
            nick = ctx.author.display_name
            username = nick.split("]")[1] if "]" in nick else nick
            username = "".join([char for char in username if char.lower() in ALLOWED_CHARS])

    uuid_request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if uuid_request.status_code > 200:
        return await error(ctx, "Error! Username was incorrect.", "Make sure you spelled the target player's name correctly")

    try:
        uuid = uuid_request.json()["id"]
    except KeyError:
        return await error(ctx, "Error! Username was incorrect.", "Make sure you spelled the target player's name correctly")


    profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()

    if profile_list['profiles'] is None:  # If we can't find any profiles, they never made one
        return await error(ctx, "That user has never joined Skyblock before!", "Make sure you typed the name correctly and try again.")

    valid_profiles = [x for x in profile_list["profiles"] if "last_save" in x['members'][uuid]]

    if not valid_profiles:
        return await error(ctx, "Error, cannot find profiles for this user!", "Make sure you spelled the target player's name correctly")
    
    profile = max(valid_profiles, key=lambda x: x['members'][uuid]['last_save'])

    profile_dict = profile["members"][uuid]

    profile_dict["uuid"] = uuid
    profile_dict["profile_id"] = profile["profile_id"]
    profile_dict["username"] = username
    profile_dict["cute_name"] = profile["cute_name"]

    return profile_dict

