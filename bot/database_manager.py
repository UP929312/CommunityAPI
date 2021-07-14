import mysql.connector
# Per guild prefixes
with open("text_files/database_creds.txt") as file:
    data = [x.rstrip("\n") for x in file.readlines()]

host, user, password = data

def load_guild_prefix(guild_id):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("SELECT prefix FROM guild_prefixes WHERE guild_id=%s", (guild_id,))
        records = cursor.fetchall()
        return (None if records == [] else records[0][0])
        
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def set_guild_prefix(guild_id, prefix):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("INSERT INTO guild_prefixes (guild_id, prefix) VALUES (%s, %s)", (guild_id, prefix))
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()


def update_guild_prefix(guild_id, prefix):
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("UPDATE guild_prefixes SET prefix=%s WHERE guild_id=%s", (prefix, guild_id))
        mydb.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def load_prefixes():
    try:
        mydb = mysql.connector.connect(host=host, user=user, password=password, database="s27_community_bot", port=3306)
        cursor = mydb.cursor()

        cursor.execute("SELECT guild_id, prefix FROM guild_prefixes")
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(e)
    finally:
        cursor.close()
#===========================================


