import requests
import json

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}

user = 0
username = test_usernames[user]

API_KEY = "8b31eff6-6407-416a-a0bd-8afa39b262c2"


#a = requests.get("https://api.hypixelskyblock.de/api/v1/cb/pages/balt")

#username = "ycarusishere"
#username = "KebabOnNaan"
#username = "ItzAlpha__"
#username = "balt"
#username = "455fcc3f87ea4a92a6c38e190c39d8ec"
username = "56ms"
#username = "Refraction"
#username = "seattle72"
#username = "Skezza"
#username = "laachs"
#username = "glai"
username = "lk"

uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"]
#uuid = "c3b9402747b1433d8b20cd54c7da3f5d"
profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()

ip = "127.0.0.1"  #  For running locally
#ip = "db.superbonecraft.dk"  # For the server

a = requests.post(f"http://{ip}:8000/pages/{uuid}", json=profile_data)
#a = requests.post(f"http://{ip}:8000/tree/{uuid}", json=profile_data)

print(a.status_code)
print(a.json())
