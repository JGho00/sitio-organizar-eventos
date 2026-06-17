import models.escuela as escuela_model
from fastapi import APIRouter,Depends,Form,HTTPException
from fastapi import Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.endopoints.dependencias import obtener_usuario_actual

#IMPORT MODELOS
from sqlmodel import Session
from core.config import obterner_sesion
from models.model_escuela import Escuela

import os

router = APIRouter(
    prefix="/escuelas",
    tags=["Escuelas"]
)


templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/",response_class=HTMLResponse)
def listar_escuelas(request: Request,username = Depends(obtener_usuario_actual)):

    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuela_model.escuelas,
            'username':username
        }
    )

@router.get("/agregar-escuela")
def agregar_escuela(request: Request,username = Depends(obtener_usuario_actual),
                    ):
    
    return templates.TemplateResponse(
        request=request,
        name="escuelas/cargar_escuela.html",
        context={
            "escuelas": escuela_model.escuelas,
            "username": username
        }
    )



@router.get("/{id}")
def obtener_escuela_por_id(id: int, request: Request):
    
    
    for escuela in escuela_model.escuelas:
        if escuela.id == id:
            return templates.TemplateResponse(
                request=request,
                name="escuelas/escuela.html",
                context={
                    "escuela": escuela
                }
            )

    return {"error": "Escuela no encontrada"}




@router.post("/agregar-escuela")
def agregar_escuela(request: Request,
                    nombre:str = Form(...),
                    direccion:str= Form(...),
                    ciudad:str = Form(...),
                    telefono:str = Form(...),
                    # 1. AGREGAR LA SESIÓN AQUÍ COMO PARÁMETRO
                    sesion_bd: Session = Depends(obterner_sesion) 
                    ):
    

    escuela_nueva = Escuela(nombre=nombre,ciudad=ciudad,direccion=direccion,telefono=telefono)
    escuela_model.escuelas.append(escuela_nueva)



    #################### Creacion del modelo en BD ####################
    escuela_nueva = Escuela(
        nombre=nombre,
        direccion=direccion,
        ciudad=ciudad,
        telefono=telefono,
        año=2026  # Agrega campos obligatorios faltantes si tu modelo los pide
    )
    
    # 3. GUARDAR EN LA BASE DE DATOS
    sesion_bd.add(escuela_nueva)
    sesion_bd.commit()
    sesion_bd.refresh(escuela_nueva)


    return templates.TemplateResponse(
        request=request,
        name="escuelas/escuelas.html",
        context={
            "escuelas": escuela_model.escuelas
        }
    )

@router.post("/actualizar-escuela/{id_escuela}")
def actualizar_escuela(
                    request:Request,
                    id_escuela:int,
                    direccion:str = Form(...),
                    telefono:str = Form(...)
                       ):
    
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
def eliminar_escuela(id_escuela: int,request: Request):
    print(id_escuela)
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









