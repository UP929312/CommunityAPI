from pydantic import BaseModel
from pydantic.typing import Literal
from enum import Enum
from typing import Union

default_response_types = {
    401: {"description": "Invalid profile given. That player hasn't got a profile with that name."},
    402: {"description": "No profiles found for the given profile_data."},
    404: {"description": "UUID couldn't be found on that profile."},
    500: {"description": "An internal exception occured."},
}

###################################################

class custom_body(BaseModel):
    success: str
    profiles: list[dict]

class Item(BaseModel):
    total: int
    value: dict
    item: dict

class Total(BaseModel):
    total: int

class PriceGroup(BaseModel):
    total: int
    prices: list[Item]

class ProfileData(BaseModel):
    profile_name: Literal['Apple | Banana | Blueberry | Coconut | Cucumber | Grapes | Kiwi | Lemon | Lime | Mango | Orange | Papaya | Pear | Peach | Pineapple | Pomegranate | Raspberry | Strawberry | Tomato | Watermelon | Zucchini']
    profile_type: Literal['regular | ironman']

###################################################
class PagesOut(BaseModel):
    profile_data: ProfileData
    purse: Total
    banking: Total
    inventory: PriceGroup
    accessories: PriceGroup
    ender_chest: PriceGroup
    armor: PriceGroup
    wardrobe: PriceGroup
    vault: PriceGroup
    storage: PriceGroup
    pets: PriceGroup
#==========================
class TotalOut(BaseModel):
    total: int
#==========================
class GroupsOut(BaseModel):
    profile_data: ProfileData
    purse: int
    banking: int
    inventory: int
    accessories: int
    ender_chest: int
    armor: int
    wardrobe: int
    vault: int
    storage: int
    pets: int
#==========================
class DumpOut(BaseModel):
    pass
#==========================
class TreeOut(BaseModel):
    data: str
#===========================
'''
with open("example_profile_data.txt", "r") as file:
    example_profile_data = file.read()
    
pages_example_inputs = {
    "Pages for 56ms": {
        "summary": "Pages for 56ms",
        #"description": "A **normal** item works correctly.",
        "value": {
            "uuid": "1277d71f338046e298d90c9fe4055f00",
            "profile": "Strawberry",
            "body": example_profile_data,
        },
    },
}
''' 
