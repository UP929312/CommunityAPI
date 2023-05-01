import requests
import json

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}

user = 0
username = test_usernames[user]

# Skezza
API_KEY = "78a53e82-85b5-442f-89cd-744285cbce80"


#a = requests.get("https://api.hypixelskyblock.de/api/v1/cb/pages/balt")

# Leaderboard players:
#username = "NewEriwan"
username = "Minikloon"
#username = "Refraction"
#username = "fela22"
#username = "Makiso"
username = "DeathStreeks"
username = "Repurposer"
username = "StutterMuch"
username = "Ealman"
username = "Skezza"
#username = "oNicNoc"
#username = "56ms"
#username = "ycarusishere"
#username = "KebabOnNaan"
#username = "ItzAlpha__"
#username = "balt"
#username = "455fcc3f87ea4a92a6c38e190c39d8ec"
#username = "seattle72"
#username = "laachs"
#username = "glai"
#username = "lk"
#username = "AndtheBand28"
#username = "JasonHYH186"
#username = "Jomis_"
#username = "Everlasting_Luck"


uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]

#uuid = "1e82592262494e8fb814dffb7de916aa"
#uuid = "0cb78dbf35e84a77bad937199a1a91ef"
profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}")
if profile_data.status_code != 200:
    print(f"Key dead? Status code: {profile_data.status_code}")
    print(profile_data.text)

profile_json = profile_data.json()

ip = "127.0.0.1"  #  For running locally
#ip = "panel.skyblockcommunity.com"
#ip = "db.superbonecraft.dk"  # For the server

print("Before")
a = requests.post(f"http://{ip}:8000/pages/{uuid}", json=profile_json)
print("After")
#a = requests.post(f"http://{ip}:8000/tree/{uuid}", json=profile_data)

print(a.status_code)
print(a.json())
