from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every ###

from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from endpoints.total import get_total_value
from endpoints.groups import get_groups_value
from endpoints.pages import get_pages_dict
from endpoints.dump import get_dump_dict
from endpoints.debug import get_debug_values
from endpoints.tree import get_tree

from data.constants.jerry_price_list import PRICES###
from data.constants.lowest_bin import LOWEST_BIN###
from data.constants.bazaar import BAZAAR###
from data.constants.collector import fetch_prices###

import uvicorn
import os###

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data:
    pass

@app.on_event("startup")
@repeat_every(seconds=60*60)  # 1 hour
def update_price_lists() -> None:
    print("Updating prices:")
    cwd = os.getcwd()
    os.chdir('data/constants')
    Data.BAZAAR, Data.LOWEST_BIN, Data.PRICES = fetch_prices()########
    os.chdir(cwd)

@app.get("/")
@limiter.limit("20/minute")
async def root(request: Request):
    return JSONResponse(status_code=200, content={"message": "Hello world!"})


@app.get("/online")
@limiter.limit("20/minute")
async def test_online(request: Request):
    return JSONResponse(status_code=200, content={"message": "API Operational"})


@app.get("/error")
async def error(request: Request):
    return JSONResponse(status_code=400, content={"message": "Item not found"})


@app.get("/total/{username}")
async def total(request: Request, username: str):
    total = await get_total_value(Data, username)
    if isinstance(total, dict):
        return JSONResponse(status_code=200, content=total)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"})       


@app.get("/groups/{username}")
async def groups(request: Request, username: str):
    groups = await get_groups_value(Data, username)
    if isinstance(groups, dict):
        return JSONResponse(status_code=200, content=groups)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"})  


@app.get("/pages/{username}")
async def pages(request: Request, username: str):
    pages = await get_pages_dict(Data, username)
    if isinstance(pages, dict):
        return JSONResponse(status_code=200, content=pages)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 


@app.get("/dump/{username}")
async def dump(request: Request, username: str):
    dump = await get_dump_dict(Data, username)
    if isinstance(dump, dict):
        return JSONResponse(status_code=200, content=dump)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 


@app.get("/debug/{username}")
async def debug(request: Request, username: str):
    debug_values = await get_debug_values(Data, username)
    if isinstance(debug_values, dict):
        return JSONResponse(status_code=200, content=debug_values)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 

@app.get("/tree/{username}")
async def tree(request: Request, username: str):
    tree_data = await get_tree(Data, username)
    if isinstance(tree_data, dict):
        return JSONResponse(status_code=200, content=tree_data)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 

if __name__ == "__main__":
    print("Done")
    uvicorn.run(app, host='0.0.0.0', port=8000, debug=True)
