# api/dependencies.py
from fastapi import Request, HTTPException, status,Depends
from sqlmodel import Session

from fastapi.responses import RedirectResponse

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

    if not cookie_token:
        print("COOKIE")
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    try:
        token = cookie_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            print("TOKEN")
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

        # 2. Buscamos el objeto Usuario completo en PostgreSQL usando el username

        usuario:Usuario = await obtener_usuario_activo_bd(sesion,username)

        if usuario is None:
            PRINT("BD")
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

        # 3. Devolvemos el objeto de la base de datos, NO un string
        return usuario
            
    except Exception:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    

#Validacion Rol

class VerificarRol:
    def __init__(self, roles_permitidos: list[str]):
        """Recibe la lista de roles que tienen permiso, ej: ['admin', 'editor']"""
        self.roles_permitidos = roles_permitidos

    def __call__(self, usuario_actual: Usuario = Depends(obtener_usuario_actual)) -> Usuario:
        try:
            print("USUARIO",usuario_actual)
            if usuario_actual.rol not in self.roles_permitidos:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes los permisos necesarios para realizar esta acción."
                )
            
            #print(f"Usuario actualbd :{usuario_actual}")
            return usuario_actual
        except Exception as e:
            
            raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"}
        )



listado_cuotas:list = [3,6,9,12,18,24,36]