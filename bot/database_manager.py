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
# For settings prefixes
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
# For linking accounts
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
# For leaderboard and adding them
def insert_profile(uuid, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets):
    execute_command('''INSERT INTO stored_profiles (uuid, datetime, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets)
                     VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (uuid, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets))

def get_saved_profiles(uuid, time=datetime.datetime(2000, 1, 1)):  # Basically, a long time ago
    return fetch_data("SELECT datetime, purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets FROM stored_profiles WHERE uuid=%s AND datetime > %s", (uuid, time))

def get_max_networth_all_time():
    return fetch_data('''
        SELECT uuid, MAX(purse+banking+inventory+accessories+ender_chest+armor+vault+wardrobe+storage+pets) as total
        FROM stored_profiles
        GROUP BY uuid
        ORDER BY total
        DESC
        LIMIT 12
    ''')

def get_max_current_networth():
    return fetch_data('''
        SELECT t1.uuid, (t1.purse+t1.banking+t1.inventory+t1.accessories+t1.ender_chest+t1.armor+t1.vault+t1.wardrobe+t1.storage+t1.pets) AS total FROM 
        stored_profiles AS t1 INNER JOIN (
          SELECT t3.uuid, MAX(t3.datetime) AS datetime
          FROM stored_profiles AS t3
          GROUP BY t3.uuid
        ) AS t2 ON t1.uuid = t2.uuid AND t1.datetime = t2.datetime
        ORDER BY total DESC LIMIT 12
    ''')
#===========================================
# For rank
def get_specific_networth_data(uuid):
    return fetch_data('''
        SELECT purse, banking, inventory, accessories, ender_chest, armor, vault, wardrobe, storage, pets
        FROM stored_profiles 
        WHERE uuid = %s
        ORDER BY datetime DESC
        LIMIT 1
    ''', (uuid,))

def get_all_networth_data():
    return fetch_data('''
        SELECT t1.purse, t1.banking, t1.inventory, t1.accessories, t1.ender_chest, t1.armor, t1.vault, t1.wardrobe, t1.storage, t1.pets FROM 
        stored_profiles AS t1 INNER JOIN (
          SELECT t3.uuid, MAX(t3.datetime) AS datetime
          FROM stored_profiles AS t3
          GROUP BY t3.uuid
        ) AS t2 ON t1.uuid = t2.uuid AND t1.datetime = t2.datetime
    ''')

def get_sum_networth_data():
    return fetch_data('''
        SELECT (t1.purse+t1.banking+t1.inventory+t1.accessories+t1.ender_chest+t1.armor+t1.vault+t1.wardrobe+t1.storage+t1.pets) FROM 
        stored_profiles AS t1 INNER JOIN (
          SELECT t3.uuid, MAX(t3.datetime) AS datetime
          FROM stored_profiles AS t3
          GROUP BY t3.uuid
        ) AS t2 ON t1.uuid = t2.uuid AND t1.datetime = t2.datetime
    ''')



