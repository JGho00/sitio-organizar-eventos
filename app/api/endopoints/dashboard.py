from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request,status
from fastapi.responses import RedirectResponse
from api.endopoints.dependencias import obtener_usuario_actual
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["dashboard"],
    prefix="/dashboard"
)


@router.get("/")
async def cargar_dashboard(request:Request,username = Depends(obtener_usuario_actual)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    response =  templates.TemplateResponse(
        request=request,
        name="dashboard/dashboard.html",
        context= {
            "request":request,
            "username": username,
            
                }
            
    )

    print(response.context)

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