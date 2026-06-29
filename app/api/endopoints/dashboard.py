from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from api.endopoints.dependencias import obtener_usuario_actual
templates = Jinja2Templates("templates")

router = APIRouter(
    tags= ["dashboard"],
    prefix="/dashboard"
)


@router.get("/")
async def cargar_dashboard(request:Request,username = Depends(obtener_usuario_actual)):
    

    
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