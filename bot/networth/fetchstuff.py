import discord  # type: ignore
from discord.ext import commands  # type: ignore
from discord.commands import Option  # type: ignore
from typing import Optional

import requests

from utils import API_KEY
def fetch_skyblock_level(username):
    url = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()
    uuid = url['id']
    try:
        profile_list = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
        valid_profiles = [x for x in profile_list["profiles"] if uuid in x['members'] and "selected" in x]    
        profile = max(valid_profiles, key=lambda x: x['selected'])
        level = profile["members"][uuid]["leveling"]["experience"]
        return int(level)
    except:
        return 0 
def emojisforlevel(level):
    if level > 360:
        return 'Very Special [🔴]'
    elif level > 320:
        return 'Special 🟥'
    elif level > 280:
        return 'Divine 🟦'
    elif level > 240:
        return 'Mythic <:pink_square:1073051068998623342>'
    elif level > 200:
        return 'Legendary 🟨'
    elif level > 160:
        return 'Epic 🟪'
    elif level > 120:
        return 'Rare 🟦'
    elif level > 80:
        return 'Uncommon 🟩'
    elif level > 40:
        return 'Common ⬜'
def permissions(level, username):
    if level <= 3:
        return f'{username} does not have access to Wardrobe, Garden, Bazaar, Auto-Pickup and Community Shop. {username} lacks progression, or has created a new profile.'
    elif level <= 5:
        return f'{username} does not have access to Bazaar, Auto-Pickup and Garden.'
    elif level <= 6:
        return f'{username} does not have have acccess to Bazaar.'    
    else:
        return ''

def decimal_part(num):
    realnumber = num/100
    num1 = realnumber - int(realnumber)
    times100 = num1*100
    round1 = round(int(times100))
    return round1
