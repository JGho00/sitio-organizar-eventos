from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
cod_1_token = "ajshdajshdjhasdkjhaskdjhaskjdhakd"
cod_2_token = "32423HJSDJFHSAJHMNASMNDASDasdjhajdjahsdas"
templates = Jinja2Templates("templates")

router = APIRouter(
    prefix='/dashboard',
    tags= ["dashboard"]
)


@router.get("/")
async def cargar_dashboard(request:Request,username = Depends(obtener_usuario_actual)):
    
    username = username.replace(cod_1_token,'').replace(cod_2_token,'').strip()
    print(username)
    
    response =  templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context= {
            "request":request,
            "username": username
                }
    )

    return response
