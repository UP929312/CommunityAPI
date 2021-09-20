from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

'''###
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
#'''###

from endpoints.pages import get_pages_dict
from endpoints.total import get_total_value
from endpoints.groups import get_groups_value
from endpoints.dump import get_dump_dict
from endpoints.tree import get_tree

from exceptions import InvalidApiKeyException, InvalidUsername, MojangServerError
from base_models import default_response_types, PagesOut, TotalOut, GroupsOut, DumpOut, TreeOut

from data.constants.collector import fetch_prices
#from price_list_updater import update_price_lists

import uvicorn
import aiohttp

app = FastAPI()

'''###
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
#'''###

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
class Data:
    pass

class Session:
    pass

data = Data()
session_object = Session()

@app.on_event("startup")
async def create_session() -> None:
    session_object.session = aiohttp.ClientSession()

@app.on_event("startup")
@repeat_every(seconds=60*60, raise_exceptions=True)  # 1 hour
def update_price_lists_loop() -> None:
    print("Updating price lists loop")

    #data = update_price_lists(data)

    #'''
    data.BAZAAR, data.LOWEST_BIN, data.PRICES, data.NPC_ITEMS = fetch_prices()
    data.BAZAAR["ENDER_PEARL"] = 100
    data.BAZAAR["ENCHANTED_CARROT"] = 1000
    # For overrides
    for item, hard_price in [("RUNE", 5), ("WISHING_COMPASS", 1000), ("PLUMBER_SPONGE", 100), ("ICE_HUNK", 100),]:
        data.LOWEST_BIN[item] = hard_price
    # Price backups
    for item, hard_price in [("SCATHA;2", 250_000_000),("SCATHA;3", 500_000_000), ("SCATHA;4", 1_000_000_000 ), ("GAME_ANNIHILATOR", 2_500_000_000), ("GAME_BREAKER", 1_000_000_000), ]:
        if item not in data.LOWEST_BIN:
            data.LOWEST_BIN[item] = hard_price
    #'''

async def validate(function, params):
    try:
        returned_data = await function(*params)
        if isinstance(returned_data, dict):
            return JSONResponse(status_code=200, content=returned_data)

        print("ERROR!")
        return JSONResponse(status_code=500, content={"message": "An internal exception occured."})
    except InvalidApiKeyException:
        return JSONResponse(status_code=401, content={"message": "An invalid API key was passed. Please try another key."})
    except InvalidUsername:
        return JSONResponse(status_code=404, content={"message": "Username could not be found."})
    except MojangServerError:
        return JSONResponse(status_code=503, content={"message": "Mojang's servers didn't respond."})
    except:
        return JSONResponse(status_code=500, content={"message": "An internal exception occured."})
        
        
@app.get("/pages/{username}", response_model=PagesOut, responses=default_response_types)
async def pages(request: Request, username: str, api_key: str):
    """
    Returns each category's total, as well as the top 5 most expensive items from each catagory.

    - **username**: the player you want to check
    - **api_key**: a hypixel api key (generated with /api new)
    """
    return await validate(get_pages_dict, (session_object.session, api_key, data, username))


@app.get("/total/{username}", response_model=TotalOut, responses=default_response_types)
async def total(request: Request, username: str, api_key: str):
    """
    Returns the combined total including purse, banking and all inventories,
    with a single "total" field.

    - **username**: the player you want to check
    - **api_key**: a hypixel api key (generated with /api new)
    """
    return await validate(get_total_value, (session_object.session, api_key, data, username))


@app.get("/groups/{username}", response_model=GroupsOut, responses=default_response_types)
async def groups(request: Request, username: str, api_key: str):
    """
    Returns a map of all containers and their corrosponding totals.
    
    - **username**: the player you want to check
    - **api_key**: a hypixel api key (generated with /api new)
    """
    return await validate(get_groups_value, (session_object.session, api_key, data, username))  


@app.get("/dump/{username}", deprecated=True)
async def dump(request: Request, username: str, api_key: str):
    """
    Returns a complete dump off *all* item data, the prices and their parsed data.
    
    - **username**: the player you want to check
    - **api_key**: a hypixel api key (generated with /api new)
    """
    return await validate(get_dump_dict, (session_object.session, api_key, data, username))  


@app.get("/tree/{username}", response_model=TreeOut, responses=default_response_types)
async def tree(request: Request, username: str, api_key: str):
    """
    Returns a tree-like structure to aid in visualising the output data,
    returned with new line characters and calculated spacing.
    
    - **username**: the player you want to check
    - **api_key**: a hypixel api key (generated with /api new)
    """
    return await validate(get_tree, (session_object.session, api_key, data, username))


@app.get("/")
async def root(request: Request):
    return JSONResponse(status_code=200, content={"message": "Hello world!"})


@app.get("/online")
async def test_online(request: Request):
    """
    A quick endpoint to test the status of the endpoint, should return a regular 200 status code.
    """
    return JSONResponse(status_code=200, content={"message": "API Operational"})


if __name__ == "__main__":
    print("Done")
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)
