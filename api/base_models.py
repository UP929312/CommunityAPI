from pydantic import BaseModel

from typing import Union

default_response_types = {
    401: {"description": "An invalid API key was passed. Please try another key."},
    404: {"description": "Username could not be found."},
    500: {"description": "An internal exception occured."},
    503: {"description": "Mojang's servers didn't respond."},
}

###################################################

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
    profile_name: str
    profile_type: str

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
    
