
from fastapi import FastAPI

from app.users.router import router as router_users
from app.friends.router import router as router_friend_req
from app.maps.router import router as router_maps

app = FastAPI()

app.include_router(router_users)
app.include_router(router_friend_req)
app.include_router(router_maps)
