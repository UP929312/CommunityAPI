from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from endpoints.total import get_total_value
from endpoints.groups import get_groups_value
from endpoints.pages import get_pages_dict
from endpoints.dump import get_dump_dict
from endpoints.debug import get_debug_values

import uvicorn

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@limiter.limit("5/minute")
async def total(request: Request, username: str):
    total = await get_total_value(username)
    if isinstance(total, dict):
        return JSONResponse(status_code=200, content=total)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"})       

@app.get("/groups/{username}")
@limiter.limit("5/minute")
async def groups(request: Request, username: str):
    groups = await get_groups_value(username)
    if isinstance(groups, dict):
        return JSONResponse(status_code=200, content=groups)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"})  

@app.get("/pages/{username}")
@limiter.limit("5/minute")
async def pages(request: Request, username: str):
    pages = await get_pages_dict(username)
    if isinstance(pages, dict):
        return JSONResponse(status_code=200, content=pages)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 

@app.get("/dump/{username}")
@limiter.limit("5/minute")
async def dump(request: Request, username: str):
    dump = await get_dump_dict(username)
    if isinstance(dump, dict):
        return JSONResponse(status_code=200, content=dump)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 


@app.get("/debug/{username}")
@limiter.limit("5/minute")
async def debug(request: Request, username: str):
    debug_values = await get_debug_values(username)
    if isinstance(debug_values, dict):
        return JSONResponse(status_code=200, content=debug_values)
    return JSONResponse(status_code=400, content={"message": "Username could not be found!"}) 

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.0', port=8000, debug=True)
