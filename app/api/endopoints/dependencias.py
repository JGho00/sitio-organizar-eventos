# api/dependencies.py
from fastapi import Request, HTTPException, status
import jwt

from core.config import SECRET_KEY,ALGORITHM

async def obtener_usuario_actual(request: Request) -> str:
    """
    Dependencia global. Revisa la cookie 'access_token'.
    Si no existe o es inválida, redirige al usuario a la página de login.
    """
    cookie_token = request.cookies.get("access_token")
    
    if not cookie_token:
        return None
    
    try:
        # Quitamos la palabra 'Bearer ' para quedarnos solo con el string del token
        token = cookie_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except Exception:
        return None
    