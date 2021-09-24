import requests
import json
import unittest
from parameterized import parameterized, parameterized_class

ip = "http://127.0.0.1:8000"  #  For running locally
#ip = "http://db.superbonecraft.dk:8000"  # For the server

API_KEY = ""

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  4: "Skezza", 5: "kori_100",
                  6: "Zaptro",
                  7: "seattle72", 8: "Refraction", 9: "laachs"}

uuids = [requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()["id"] for username in test_usernames.values()]

DEFAULT_KEYS = ["profile_data", "purse", "banking", "inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"]

def get_profile_data(uuid):
    profile_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={API_KEY}&uuid={uuid}").json()
    return profile_data

@parameterized_class(
    ("uuid"),
    [(x,) for x in uuids],
)
class TotalEndpoint(unittest.TestCase):

    print("Testing")

    #@unittest.skip("Skip")
    def test_a_total(self):
        profile_data = get_profile_data(self.uuid)
        r = requests.post(f"{ip}/total/{self.uuid}", json=profile_data)
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check that it's {"total": x}
        self.assertEqual(list(r.keys()) == ["total"], True)
        # Check that it's only {"total": x}
        self.assertEqual(len(r.keys()), 1)
        # Check that the total isn't a string or None
        self.assertEqual(isinstance(r["total"], int), True)

    #@unittest.skip("Skip")
    def test_b_groups(self):
        profile_data = get_profile_data(self.uuid)
        r = requests.post(f"{ip}/groups/{self.uuid}", json=profile_data)
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)

    #@unittest.skip("Skip")
    def test_c_pages(self):
        profile_data = get_profile_data(self.uuid)
        r = requests.post(f"{ip}/pages/{self.uuid}", json=profile_data)
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)

    #@unittest.skip("Skip")
    def test_d_dump(self):
        profile_data = get_profile_data(self.uuid)
        r = requests.post(f"{ip}/dump/{self.uuid}", json=profile_data)
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)
        
if __name__ == '__main__':
    print("Starting tests")
    unittest.main()
