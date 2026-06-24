from sqlmodel import SQLModel,Session,select
from fastapi import Depends

from models.model_usuario import Usuario



async def obtener_usuarios_bd(sesion:Session):
    consulta = select(Usuario)
    usuarios = sesion.exec(consulta).all()
    return usuarios
    


async def obtener_usuario_id_bd(sesion:Session,id_usuario:int):
    
    consulta = select(Usuario).where(Usuario.id_usuario== id_usuario)

    usuario = sesion.exec(consulta).first()

    return usuario

async def crear_usuario_bd(sesion:Session,username:str,email:str,password_hash:str,rol:str):
    
    usuario_nuevo = Usuario(username=username,email=email,password_hash=password_hash,rol=rol)
    sesion.add(usuario_nuevo)
    sesion.commit()
    sesion.refresh(usuario_nuevo)

    return usuario_nuevo

async def actualizar_usuario_id_bd(sesion:Session,id_usuario:int,username:str,password_hash:str,email:str,rol:str):
    
    usuario:Usuario = await obtener_usuario_id_bd(sesion,id_usuario)
    if usuario:
        usuario.username = username
        usuario.password_hash = password_hash
        usuario.email = email
        usuario.rol = rol
        

        sesion.add(usuario)
        sesion.commit()
        sesion.refresh(usuario)

        return usuario

async def eliminar_usuario_bd(sesion:Session,id_usuario:int):
    
    usuario = await obtener_usuario_id_bd(sesion,id_usuario)
    if usuario:
        sesion.delete(usuario)
        sesion.commit()
        return usuario


def crear_hash_usuario(password:str):
    return password


def consultar_hash(password:int,password_hash:str):
    #BD
    usuario_enontrado:False

    return usuario_enontrado 

def obtener_usuario(db,username):
     if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)