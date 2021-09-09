import requests
import json
import unittest
from parameterized import parameterized, parameterized_class

ip = "http://127.0.0.1:8000"  #  For running locally
#ip = "http://db.superbonecraft.dk:8000"  # For the server

test_usernames = {0: "56ms", 1: "nonbunary", 2: "poroknights",
                  4: "Skezza", 5: "kori_100",
                  #6: "XD_Zaptro_XD",
                  7: "seattle72", 8: "Refraction"}

DEFAULT_KEYS = ["purse", "banking", "inventory", "accessories", "ender_chest", "armor", "wardrobe", "vault", "storage", "pets"]

@parameterized_class(
    ("username"),
    [(x,) for x in test_usernames.values()],
)
class TotalEndpoint(unittest.TestCase):

    #@unittest.skip("Skip")
    def test_a_total(self):
        r = requests.get(f"{ip}/total/{self.username}")
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
        r = requests.get(f"{ip}/groups/{self.username}")
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)

    #@unittest.skip("Skip")
    def test_c_pages(self):
        r = requests.get(f"{ip}/pages/{self.username}")
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)

    #@unittest.skip("Skip")
    def test_d_dump(self):
        r = requests.get(f"{ip}/dump/{self.username}")
        # Check of OK, 200        
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for right keys
        self.assertEqual(list(r.keys()) == DEFAULT_KEYS, True)
        # Check for wrong keys
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS), True)

    #@unittest.skip("Skip")
    def test_e_debug(self):
        r = requests.get(f"{ip}/debug/{self.username}")
        # Check of OK, 200
        self.assertEqual(r.status_code, 200)
        r = r.json()
        # Check for wrong keys (include total)
        self.assertEqual(len(r.keys()) == len(DEFAULT_KEYS)+1, True)
        
if __name__ == '__main__':
    print("Starting tests")
    unittest.main()
