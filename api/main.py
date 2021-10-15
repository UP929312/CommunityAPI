from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi_utils.tasks import repeat_every


from endpoints.pages import get_pages_dict
from endpoints.total import get_total_value
from endpoints.groups import get_groups_value
from endpoints.dump import get_dump_dict
from endpoints.tree import get_tree

from exceptions import InvalidProfileException, NoProfilesException, InvalidUUIDException
from base_models import custom_body, default_response_types, PagesOut, TotalOut, GroupsOut, DumpOut, TreeOut

from data.constants.collector import fetch_prices

import uvicorn

app = FastAPI()

BAZAAR_CAPS = {
    "CARROT_ITEM":26, "ENCHANTED_CARROT":2999, "ENCHANTED_GOLDEN_CARROT":421169,
    "POTATO_ITEM":28, "ENCHANTED_POTATO":2672, "ENCHANTED_BAKED_POTATO":362046,
    "NETHER_STALK":38, "ENCHANTED_NETHER_STALK":4800, "MUTANT_NETHER_STALK":767221,
    "WHEAT":31, "ENCHANTED_HAY_BLOCK":40882, "TIGHTLY_TIED_HAY_BALE":4749995,
    "SUGAR_CANE":22, "ENCHANTED_SUGAR_CANE":543001, "ENCHANTED_SUGAR":3299,   
    "HAY_BLOCK":984,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
class Data:
    pass

data = Data()

@app.on_event("startup")
@repeat_every(seconds=60*60, raise_exceptions=True)  # 1 hour
def update_price_lists_loop() -> None:
    print("Updating price lists loop")

    data.BAZAAR, data.LOWEST_BIN, data.PRICES, data.NPC_ITEMS = fetch_prices()
    data.BAZAAR["ENDER_PEARL"] = 100
    for item, price in BAZAAR_CAPS.items():
        if data.BAZAAR[item] > price:
            data.BAZAAR[item] = price-price*0.25
    # For overrides
    for item, hard_price in [("RUNE", 5), ("WISHING_COMPASS", 1000), ("ICE_HUNK", 100),]:
        data.LOWEST_BIN[item] = hard_price
    # Price backups
    for item, hard_price in [("SCATHA;2", 250_000_000),("SCATHA;3", 500_000_000), ("SCATHA;4", 1_000_000_000 ), ("GAME_ANNIHILATOR", 2_500_000_000), ("GAME_BREAKER", 1_000_000_000), ]:
        if item not in data.LOWEST_BIN:
            data.LOWEST_BIN[item] = hard_price

async def validate(function, params):
    try:
        returned_data = await function(*params)
        if isinstance(returned_data, dict):
            return JSONResponse(status_code=200, content=returned_data)

        print("ERROR!")
        return JSONResponse(status_code=500, content={"message": "An internal exception occured."})
    
    except InvalidProfileException:
        return JSONResponse(status_code=401, content={"message": "Invalid profile given. That player hasn't got a profile with that name."})
    except NoProfilesException:
        return JSONResponse(status_code=402, content={"message": "No profiles found for the given profile_data."})
    except InvalidUUIDException:
        return JSONResponse(status_code=404, content={"message": "UUID couldn't be found on that profile."})
    except:
        return JSONResponse(status_code=500, content={"message": "An internal exception occured."})
        
        
@app.post("/pages/{uuid}", response_model=PagesOut, responses=default_response_types)
async def pages(request: Request, uuid: str, profile_data: custom_body, profile_name: str = None):  #  = Body(..., examples=pages_example_inputs)
    """
    Returns each category's total, as well as the top 5 most expensive items from each catagory.

    - **uuid**: the player you want to target
    - **profile_name**: (optional) the profile you watch to target

    Request body:<br>
    ⠀⠀⠀⠀The body needs to be a user's profile data, sent over in JSON format. It should be a jsonified version of the<br>
    ⠀⠀⠀⠀response that is sent from https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}
    """
    return await validate(get_pages_dict, (data, profile_data.profiles, uuid, profile_name))


@app.post("/total/{uuid}", response_model=TotalOut, responses=default_response_types)
async def total(request: Request, uuid: str, profile_data: custom_body, profile_name: str = None):
    """
    Returns the combined total including purse, banking and all inventories,
    with a single "total" field.

    - **uuid**: the player you want to target
    - **profile_name**: (optional) the profile you watch to target

    Request body:<br>
    ⠀⠀⠀⠀The body needs to be a user's profile data, sent over in JSON format. It should be a jsonified version of the<br>
    ⠀⠀⠀⠀response that is sent from https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}
    """
    return await validate(get_total_value, (data, profile_data.profiles, uuid, profile_name))


@app.post("/groups/{uuid}", response_model=GroupsOut, responses=default_response_types)
async def groups(request: Request, uuid: str, profile_data: custom_body, profile_name: str = None):
    """
    Returns a map of all containers and their corresponding totals.
    
    - **uuid**: the player you want to target
    - **profile_name**: (optional) the profile you watch to target

    Request body:<br>
    ⠀⠀⠀⠀The body needs to be a user's profile data, sent over in JSON format. It should be a jsonified version of the<br>
    ⠀⠀⠀⠀response that is sent from https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}
    """
    return await validate(get_groups_value, (data, profile_data.profiles, uuid, profile_name))  


@app.post("/dump/{uuid}", response_model=PagesOut, responses=default_response_types)
async def dump(request: Request, uuid: str, profile_data: custom_body, profile_name: str = None):
    """
    Returns a complete dump off *all* item data, the prices and their parsed data.
    
    - **uuid**: the player you want to target
    - **profile_name**: (optional) the profile you watch to target
    """
    return await validate(get_dump_dict, (data, profile_data.profiles, uuid, profile_name))  


@app.post("/tree/{uuid}", response_model=TreeOut, responses=default_response_types, include_in_schema=False)
async def tree(request: Request, uuid: str, profile_data: custom_body, profile_name: str = None):
    """
    Returns a tree-like structure to aid in visualising the output data,
    returned with new line characters and calculated spacing.
    
    - **uuid**: the player you want to target
    - **profile_name**: (optional) the profile you watch to target

    Request body:<br>
    ⠀⠀⠀⠀The body needs to be a user's profile data, sent over in JSON format. It should be a jsonified version of the<br>
    ⠀⠀⠀⠀response that is sent from https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}
    """
    return await validate(get_tree, (data, profile_data.profiles, uuid, profile_name))


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return JSONResponse(status_code=200, content={"message": "Hello world!"})


@app.get("/online")
async def test_online(request: Request):
    """
    A quick endpoint to test the status of the endpoint, should return a regular 200 status code.
    """
    return JSONResponse(status_code=200, content={"message": "API Operational"})

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response("favicon.ico", media_type="image/ico")

if __name__ == "__main__":
    print("Done")
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)
