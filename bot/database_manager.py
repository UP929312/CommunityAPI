import mysql.connector
import datetime

with open("text_files/database_creds.txt") as file:
    host, user, password = [x.rstrip("\n") for x in file.readlines()]

#===========================================
def fetch_data(*args):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor(*args)

        cursor.execute(*args)
        records = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return records

def execute_command(*args):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute(*args)
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

#===========================================
def load_guild_prefix(guild_id):
    records = fetch_data("SELECT prefix FROM guild_prefixes WHERE guild_id=%s", (guild_id,))
    return (None if records == [] else records[0][0])
     
def set_guild_prefix(guild_id, prefix):
    execute_command("INSERT INTO guild_prefixes (guild_id, prefix) VALUES (%s, %s)", (guild_id, prefix))
    
def update_guild_prefix(guild_id, prefix):
    execute_command("UPDATE guild_prefixes SET prefix=%s WHERE guild_id=%s", (prefix, guild_id))
    
def load_prefixes():
    return fetch_data("SELECT guild_id, prefix FROM guild_prefixes")

#===========================================
def load_linked_account(discord_id):
    records = fetch_data("SELECT username FROM linked_accounts WHERE discord_id=%s", (discord_id,))
    return (None if records == [] else records[0][0])

def set_linked_account(discord_id, username):
    execute_command("INSERT INTO linked_accounts (discord_id, username) VALUES (%s, %s)", (discord_id, username))

def update_linked_account(discord_id, username):
    execute_command("UPDATE linked_accounts SET username=%s WHERE discord_id=%s", (username, discord_id))

def load_linked_accounts():
    return fetch_data("SELECT discord_id, username FROM linked_accounts")

#===========================================
def insert_profile(uuid, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets):
    execute_command('''INSERT INTO stored_profiles (uuid, datetime, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets)
                     VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (uuid, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets))

def get_saved_profiles(uuid, time=datetime.datetime(2000, 1, 1)):  # Basically, a long time ago
    return fetch_data("SELECT datetime, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets FROM stored_profiles WHERE uuid=%s AND datetime > %s", (uuid, time))
'''
def get_saved_profiles_dev():
    print(fetch_data("SELECT * FROM stored_profiles"))

get_saved_profiles_dev()
'''
