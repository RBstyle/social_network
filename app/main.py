from fastapi import FastAPI

from app.routers import profiles, posts, likes
from . import swagger_vars

FastAPI
app = FastAPI(
    title=swagger_vars.title,
    description=swagger_vars.description,
    summary=swagger_vars.summary,
    version=swagger_vars.version,
    openapi_tags=swagger_vars.tags_metadata,
)

app.include_router(profiles.router)
app.include_router(posts.router)
app.include_router(likes.router)


@app.get("/")
def test():
    return {"message": "It's alive!!"}
