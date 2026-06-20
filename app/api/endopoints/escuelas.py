import models.escuela as escuela_model
from fastapi import APIRouter,Depends,Form,HTTPException
from fastapi import Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.endopoints.dependencias import obtener_usuario_actual

#IMPORT MODELOS
from sqlmodel import Session
from core.config import obtener_sesion
from models.model_escuela import Escuela,obtener_escuelas_bd,obtener_escuela_id,editar_escuela_id_bd,eliminar_escuela_bd,crear_escuela

import os

router = APIRouter(
    prefix="/escuelas",
    tags=["Escuelas"]
)


templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/",response_class=HTMLResponse)
async def listar_escuelas(request: Request,username = Depends(obtener_usuario_actual),sesion_bd: Session = Depends(obtener_sesion)):

    escuelas_bd= await obtener_escuelas_bd(sesion_bd)
    print("Escuelas de bd",escuelas_bd)
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuelas_bd,
            'username':username
        }
    )

@router.get("/agregar-escuela")
def agregar_escuela(request: Request,username = Depends(obtener_usuario_actual),sesion = Depends(obtener_sesion)):
    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/cargar_escuela.html",
        context={
            "username": username
        }
    )



@router.get("/{id}")
async def obtener_escuela_por_id(id: int, request: Request,sesion: Session = Depends(obtener_sesion)):
    
    escuela_bd = await obtener_escuela_id(sesion,id=id)
    if not escuela_bd:
        return {"error": "Escuela no encontrada"}
    
    
    print("Escuela id",escuela_bd)
    print(type(escuela_bd))
    return templates.TemplateResponse(
                request=request,
                name="escuelas/escuela.html",
                context={
                    "escuela": escuela_bd
                }
            )

    




@router.post("/agregar-escuela")
async def agregar_escuela(request: Request,
                    nombre:str = Form(...),
                    direccion:str= Form(...),
                    ciudad:str = Form(...),
                    telefono:str = Form(...),
                    sesion: Session = Depends(obtener_sesion)
                    ):
    
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
                    sesion_bd: Session = Depends(obtener_sesion)
                       ):
    
    campos_valores = {
        'direccion':direccion,
        'telefono':telefono
    }
    
    await editar_escuela_id_bd(sesion_bd,id_escuela,campos_valores)

    existe_escuela:bool = False
    
    for escuela in escuela_model.escuelas:
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
            "escuelas": escuela_model.escuelas
        }
    )

@router.post("/eliminar-escuela/{id_escuela}")
async def eliminar_escuela(id_escuela: int,request: Request,sesion_bd: Session = Depends(obtener_sesion) ):
    print(id_escuela)

    await eliminar_escuela_bd(sesion_bd,id_escuela)

    for escuela in escuela_model.escuelas:
        if escuela.id == id_escuela:
            escuela_model.escuelas.remove(escuela)
            return templates.TemplateResponse(
                request=request,
                name="escuelas/escuelas.html",
                context={
                    "escuelas": escuela_model.escuelas
                }
            )
    return {"error": "Escuela no encontrada"}









