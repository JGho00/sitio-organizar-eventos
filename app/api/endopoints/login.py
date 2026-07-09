from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse

templates = Jinja2Templates("templates")

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

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
    response =  RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")

    return response