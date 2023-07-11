from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.routers.profiles import login_for_access_token, create_user
from app.db.database import get_db
from app.auth.forms import LoginForm, SignupForm
from app.schemas.profiles import CreateProfileRequestScheme

templates = Jinja2Templates(directory="app/templates")
login_template = "login.html"
signup_template = "signup.html"
router = APIRouter(prefix="/auth", tags=["login"])


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(login_template, {"request": request})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = RedirectResponse(url="/", status_code=302)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="Error!")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse(login_template, form.__dict__)
    return templates.TemplateResponse(login_template, form.__dict__)


@router.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse(signup_template, {"request": request})


@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    form = SignupForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            email = form.__dict__.get("username")
            password = form.__dict__.get("password2")
            first_name = form.__dict__.get("first_name")
            last_name = form.__dict__.get("last_name")

            new_form = CreateProfileRequestScheme.construct(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            response = RedirectResponse(url="/", status_code=302)
            await create_user(data=new_form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="Error!")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse(signup_template, form.__dict__)
    return templates.TemplateResponse(signup_template, form.__dict__)


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response
