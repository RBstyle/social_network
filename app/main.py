from fastapi import FastAPI
from app.routers import profiles, posts

app = FastAPI()

app.include_router(profiles.router)
app.include_router(posts.router)


@app.get("/")
def test():
    return {"message": "It's alive!!"}
