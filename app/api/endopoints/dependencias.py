# api/dependencies.py
from fastapi import Request, HTTPException, status,Depends
from sqlmodel import Session

from core.config import obtener_sesion

import jwt

from models.model_usuario import Usuario

from services.usuario_service import obtener_usuario_activo_bd

from core.config import SECRET_KEY,ALGORITHM

async def obtener_usuario_actual(request: Request,sesion: Session = Depends(obtener_sesion)) -> str:
    """
    Dependencia global. Revisa la cookie 'access_token'.
    Si no existe o es inválida, redirige al usuario a la página de login.
    """
    cookie_token = request.cookies.get("access_token")
    
    # Si no hay cookie o falla el token, lanzamos un error de credenciales
    excepcion_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o sesión expirada.",
    )
    
    if not cookie_token:
        raise excepcion_credenciales
    
    try:
        token = cookie_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise excepcion_credenciales
            
    except Exception:
        raise excepcion_credenciales

    # 2. Buscamos el objeto Usuario completo en PostgreSQL usando el username

    usuario:Usuario = await obtener_usuario_activo_bd(sesion,username)

    if usuario is None:
        raise excepcion_credenciales

    # 3. Devolvemos el objeto de la base de datos, NO un string
    return usuario

#Validacion Rol

class VerificarRol:
    def __init__(self, roles_permitidos: list[str]):
        """Recibe la lista de roles que tienen permiso, ej: ['admin', 'editor']"""
        self.roles_permitidos = roles_permitidos

    def __call__(self, usuario_actual: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        print("USUARIO",usuario_actual)
        if usuario_actual.rol not in self.roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción."
            )
        return usuario_actual