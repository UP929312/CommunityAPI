import requests
import json

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  3: "UrMinecraftDoggo", 4: "Skezza", 5: "kori_100",
                  6: "XD_Zaptro_XD", 7: "seattle72", 8: "Refraction"}

user = 0
username = test_usernames[user]

#ip = "http://127.0.0.1:8000"  #  For running locally
ip = "http://db.superbonecraft.dk:8000"  # For the server

#a = requests.get(f"{ip}/groups/56ms")
a = requests.get("http://db.superbonecraft.dk:8000/total/Skezza")
print(a.status_code)
print(a.json())

'''
#r = requests.get(f"http://127.0.0.1:8000/debug/56ms")
#r = requests.get(f"http://127.0.0.1:8000/debug/Refraction")
#r = requests.get(f"http://127.0.0.1:8000/debug/XD_Zaptro_XD")
print(r.status_code)
print(r.json())

for key, value in r.json().items():
    print (key+":", value)
#'''

'''
r = requests.get("http://127.0.0.1:8000/pages/56ms")
print(r.status_code)
#print(r.text)
print(r.json())#["inventory"]["prices"])#["inventory"]["prices"][0])
#'''
