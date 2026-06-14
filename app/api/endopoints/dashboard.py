from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual

templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["dashboard"],
    prefix="/dashboard"
)


@router.get("/")
async def cargar_dashboard(request:Request,username = Depends(obtener_usuario_actual)):
    
    
    print("user name acá",username)
    print(request)
    
    response =  templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context= {
            "request":request,
            "username": username
                }
    )

    return response
    


@router.get("/admin-user")
async def cargar_dashboard(request:Request,username = Depends(obtener_usuario_actual)):
    
    
    print(username)
    
    response =  templates.TemplateResponse(
        request=request,
        name="usuarios/usuarios.html",
        context= {
            "request":request,
            "username": username
                }
    )

    return response