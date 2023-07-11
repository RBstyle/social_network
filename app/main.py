from fastapi import FastAPI, Depends

from app.routers import profiles, posts, likes
from app.services.deps import get_current_user
from app.db.models import Profile
from app.schemas.profiles import UserOut

app = FastAPI()

app.include_router(profiles.router)
app.include_router(posts.router)
app.include_router(likes.router)


@app.get("/")
def test():
    return {"message": "It's alive!!"}


@app.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: Profile = Depends(get_current_user)):
    return user
