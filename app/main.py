from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.routers import profiles, posts, likes, login
from . import swagger_vars
from app.services.deps import get_current_user
from app.db.database import get_db

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
app.include_router(login.router)

templates = Jinja2Templates(directory="app/templates")
login_template = "index.html"


@app.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    data = {"request": request}
    user = await get_current_user(request=request, db=db)
    data["user"] = user
    return templates.TemplateResponse(login_template, data)
