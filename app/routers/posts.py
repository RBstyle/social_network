from fastapi import APIRouter, Depends, Query, status
from fastapi.requests import Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.db.database import get_db
from app.db.models import Post
from app.services.deps import get_current_user
from app.services.utils import check_post, own_post_list, post_list, get_likes
from app.schemas.posts import (
    PostResponseScheme,
    ChangePostRequestScheme,
)

router = APIRouter(prefix="/posts", tags=["posts"])
templates = Jinja2Templates(directory="app/templates")
posts_template = "posts/list.html"
create_post_template = "posts/create.html"


@router.post(
    "/",
    response_model=PostResponseScheme,
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    request: Request,
    db: Session = Depends(get_db),
    *,
    data: ChangePostRequestScheme,
):
    """Create post"""
    current_user = await get_current_user(request=request, db=db)
    db_post = Post(
        owner_id=current_user.id,
        title=data.title,
        content=data.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch("/", dependencies=[Depends(get_current_user)])
async def edit_post(
    request: Request,
    post_id: int = Query(None),
    db: Session = Depends(get_db),
    *,
    data: ChangePostRequestScheme,
):
    error = await check_post(request=request, post_id=post_id, db=db)

    if error:
        raise error

    post_query = db.query(Post).filter(Post.id == post_id)
    update_data = data.dict(exclude_unset=True)
    post_query.filter(Post.id == post_id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())

    return {"status": "success", "note": post_query.first()}


@router.delete("/", dependencies=[Depends(get_current_user)])
async def delete_post(
    request: Request, post_id: int = Query(None), db: Session = Depends(get_db)
):
    error = await check_post(request=request, post_id=post_id, db=db)

    if error:
        raise error

    db_post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return {"status": "success"}


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
)
async def get_posts(request: Request, db: Session = Depends(get_db)):
    data = {"request": request}
    user = await get_current_user(request=request, db=db)
    posts = await post_list(db=db)
    likes = await get_likes(db=db)
    data["user"] = user
    data["posts"] = posts
    data["likes"] = likes
    return templates.TemplateResponse(posts_template, data)


@router.get(
    "/create",
    dependencies=[Depends(get_current_user)],
)
async def create_form(request: Request, db: Session = Depends(get_db)):
    data = {"request": request}
    user = await get_current_user(request=request, db=db)
    data["user"] = user

    return templates.TemplateResponse(create_post_template, data)


@router.get("/list", dependencies=[Depends(get_current_user)])
async def get_own_post_list(request: Request, db: Session = Depends(get_db)):
    return await own_post_list(request=request, db=db)
