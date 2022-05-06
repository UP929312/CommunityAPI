import requests
import json

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}

user = 0
username = test_usernames[user]

API_KEY = "a5741dbb-ce47-4d0b-af54-ffc76fad4fae"


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
username = "oNicNoc"
#username = "56ms"
#username = "ycarusishere"
#username = "KebabOnNaan"
#username = "ItzAlpha__"
#username = "balt"
#username = "455fcc3f87ea4a92a6c38e190c39d8ec"
#username = "seattle72"
#username = "Skezza"
#username = "laachs"
#username = "glai"
#username = "lk"
#username = "AndtheBand28"
#username = "JasonHYH186"
username = "Skezza"

uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]

#uuid = "1e82592262494e8fb814dffb7de916aa"
#uuid = "c3b9402747b1433d8b20cd54c7da3f5d"
profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}")
if profile_data.status_code != 200:
    print("Key dead?")

profile_data = profile_data.json()

ip = "127.0.0.1"  #  For running locally
#ip = "db.superbonecraft.dk"  # For the server

a = requests.post(f"http://{ip}:8000/pages/{uuid}", json=profile_data)
#a = requests.post(f"http://{ip}:8000/tree/{uuid}", json=profile_data)

print(a.status_code)
print(a.json())
