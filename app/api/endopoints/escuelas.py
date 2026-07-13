from models.model_escuela import Escuela
from fastapi import APIRouter,Depends,Form,HTTPException,status
from fastapi import Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from api.endopoints.dependencias import VerificarRol

#IMPORT MODELOS
from sqlmodel import Session
from core.config import obtener_sesion
from services.escuela_service import  obtener_escuelas_bd,obtener_escuela_id,editar_escuela_id_bd,eliminar_escuela_bd,crear_escuela
import os

router = APIRouter(
    prefix="/escuelas",
    tags=["Escuelas"]
)


templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/",status_code=status.HTTP_200_OK)
async def listar_escuelas(request: Request,username = Depends(VerificarRol(['admin'])),sesion: Session = Depends(obtener_sesion)):

    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    escuelas_bd= await obtener_escuelas_bd(sesion)
    print("Escuelas de bd",escuelas_bd)
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas_bd,
            'username':username
        }
    )

@router.get("/agregar-escuela",status_code=status.HTTP_201_CREATED)
def agregar_escuela(request: Request,username = Depends(VerificarRol(['admin'])),sesion = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/cargar_escuela.html",
        context={
            "username": username.username
        }
    )



@router.get("/{id}",status_code=status.HTTP_200_OK)
async def obtener_escuela_por_id(id: int, request: Request,username = Depends(VerificarRol(['admin'])),sesion: Session = Depends(obtener_sesion)):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response

    escuela_bd = await obtener_escuela_id(sesion,id=id)
    if not escuela_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La escuela no existe en el sistema."
        )
    
    
    print("Escuela id",escuela_bd)
    print(type(escuela_bd))
    return templates.TemplateResponse(

                request=request,
                name="escuelas/escuela.html",
                context={
                    "escuela": escuela_bd,
                    "username": username
                }
            )

    




@router.post("/agregar-escuela")

async def agregar_escuela(request: Request,
                    nombre:str = Form(...),
                    direccion:str= Form(...),
                    telefono:str = Form(...),
                    sesion: Session = Depends(obtener_sesion),
                    username = Depends(VerificarRol(['admin']))
                    ):
    
    if not username:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("access_token")
        return response
    #################### Creacion del modelo en BD ####################
    await crear_escuela(sesion,nombre,direccion,telefono)

    
    escuelas =await obtener_escuelas_bd(sesion)

    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas
        }
    )

@router.post("/actualizar-escuela/{id_escuela}")
async def actualizar_escuela(
                    request:Request,
                    id_escuela:int,
                    direccion:str = Form(...),
                    telefono:str = Form(...),
                    sesion: Session = Depends(obtener_sesion),
                    username = Depends(VerificarRol(['admin']))
                       ):

    campos_valores = {
        'direccion':direccion,
        'telefono':telefono
    }
    
    await editar_escuela_id_bd(sesion,id_escuela,campos_valores)

    existe_escuela:bool = False
    
    escuelas:Escuela = await obtener_escuelas_bd(sesion)

    for escuela in escuelas:
        if escuela.id == id_escuela:
            existe_escuela = True
            escuela.direccion = direccion
            escuela.telefono = telefono
        
        
    if not existe_escuela:
        raise HTTPException(status_code=404,detail="No existe escuela")
    print("existe escuela")
    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas,
            "username":username
        }
    )

@router.post("/eliminar-escuela/{id_escuela}",status_code=status.HTTP_201_CREATED)
async def eliminar_escuela(id_escuela: int,request: Request,sesion: Session = Depends(obtener_sesion),username = Depends(VerificarRol(['admin']))):
    print(id_escuela)

    await eliminar_escuela_bd(sesion,id_escuela)

    escuelas:Escuela = await obtener_escuelas_bd(sesion)

    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas,
            "username":username
        }
    )









