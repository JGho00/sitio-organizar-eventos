from datetime import datetime, timedelta, timezone
from fastapi import APIRouter,Depends,Request
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates

import jwt
import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from typing import Annotated


from schemas.usuario import Token,User,create_access_token,authenticate_user,get_current_active_user,get_current_user,obtener_usuarios_bd
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES,obtener_sesion

templates = Jinja2Templates(directory=os.path.join("templates"))

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)



@router.post("/token")
async def login_for_access_token(
    request:Request,
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    sesion = Depends(obtener_sesion)
    
) -> Token:
    print(form_data.username,form_data.password)
    usuarios_bd:list = await obtener_usuarios_bd(sesion)
    print("Usuarios",usuarios_bd)
    user = authenticate_user(usuarios_bd, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
             
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

     # 1. Creamos una respuesta JSON limpia para el JavaScript del Frontend
    content = {"status": "success", "message": "Autenticación correcta"}
    response = JSONResponse(content=content, status_code=status.HTTP_200_OK)

    # 2. Inyectamos la cookie de forma segura que el navegador guardará automáticamente
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True,       # Bloquea ataques XSS (JavaScript no puede leerla)
        max_age=1800,        # Tiempo de vida: 30 minutos (en segundos)
        secure=False,        # Cambiar a True en producción cuando uses HTTPS
        samesite="lax"       # Mitiga ataques CSRF
    )

    return response


    


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

