from fastapi import APIRouter,Depends,Form,HTTPException
from fastapi import Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.endopoints.dependencias import VerificarRol

#IMPORT MODELOS
from sqlmodel import Session
from core.config import obtener_sesion
from schemas.usuario import crear_usuario_bd,obtener_usuarios_bd,obtener_usuario_id_bd,actualizar_usuario_id_bd,eliminar_usuario_bd

import os

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


templates = Jinja2Templates(directory=os.path.join("templates"))

@router.get("/",response_class=HTMLResponse)
async def listar_usuarios(request: Request,username = Depends(VerificarRol(['admin'])),sesion_bd: Session = Depends(obtener_sesion)):

    usuarios_bd= await obtener_usuarios_bd(sesion_bd)
    

    return templates.TemplateResponse(
        request=request,
        name="usuarios/usuarios.html",
        context={
            "usuarios": usuarios_bd,
            'username':username.username
        }
    )

@router.get("/agregar-usuario")
def agregar_usuario(request: Request,username = Depends(VerificarRol(['admin']))):
    
    return templates.TemplateResponse(
        request=request,
        name="usuarios/cargar_usuario.html",
        context={
            "username": username
        }
    )



@router.get("/{id}")
async def obtener_usuario_id(id: int, request: Request,sesion: Session = Depends(obtener_sesion),username = Depends(VerificarRol(['admin']))):
    
    pass
    

    


@router.post("/agregar-usuario")
async def agregar_usuario(request: Request,
                    username:str = Form(...),
                    email:str= Form(...),
                    password_hash:str = Form(...),
                    rol:str = Form(...),
                    sesion: Session = Depends(obtener_sesion)
                    ):
    
    #################### Creacion del modelo en BD ####################
    await crear_usuario_bd(sesion,username=username,email=email,password_hash=password_hash,rol=rol)

    
    usuarios =await obtener_usuarios_bd(sesion)

    return templates.TemplateResponse(
        request=request,
        name="usuarios/usuarios.html",
        context={
            "usuarios": usuarios
        }
    )

@router.post("/actualizar-usuario/{id_usuario}")
async def actualizar_usuario(
                    request:Request,
                    id_usuario:int,
                    username:str = Form(...),
                    password_hash:str = Form(...),
                    email:str = Form(...),
                    rol:str = Form(...),
                    sesion: Session = Depends(obtener_sesion)
                       ):
    
    usuario = await obtener_usuario_id_bd(sesion,id_usuario)

    if not usuario: 
        raise HTTPException(status_code=404,detail="No existe usuario")
    

    await actualizar_usuario_id_bd(sesion,id_usuario,username,password_hash,email,rol)
    
    print("existe usuario")

    usuarios = await obtener_usuarios_bd(sesion)
    
    return templates.TemplateResponse(
        request=request,
        name="usuarios/usuarios.html",
        context={
            "usuarios": usuarios
        }
    )

@router.post("/eliminar-usuario/{id_usuario}")
async def eliminar_usuario(id_usuario: int,request: Request,sesion: Session = Depends(obtener_sesion) ):
    
    print(id_usuario)

    await eliminar_usuario_bd(sesion,id_usuario)

    usuarios = await obtener_usuarios_bd(sesion)
    
    return templates.TemplateResponse(
            request=request,
            name="escuelas/usuarios.html",
            context={
                "usuarios": usuarios
                    }
            )
    









