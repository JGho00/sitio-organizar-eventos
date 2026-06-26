from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from models.usuario import usuarios_db

templates = Jinja2Templates("templates")
token:str = "ajshdajshdjhasdkjhaskdjhaskjdhakdUSER32423HJSDJFHSAJHMNASMNDASDasdjhajdjahsdas"

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

@router.get("/")
async def login(request:Request):
    #mensaje_error = request.session.pop("flash_error", None)
    return templates.TemplateResponse(
        request=request,
        name="login/login.html",
        context={
            "request": request
        }
    )




@router.get("/logout")
async def logout_from_login(request: Request):
    # Redirige a la ruta /logout global
    response =  RedirectResponse(url="/logout", status_code=302)
    response.delete_cookie("access_token")

    return response