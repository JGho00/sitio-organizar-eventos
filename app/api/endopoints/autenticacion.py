from datetime import datetime, timedelta, timezone
from fastapi import APIRouter,Depends
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from typing import Annotated


from schemas.usuario import Token,User,create_access_token,authenticate_user,get_current_active_user,get_current_user,obtener_usuarios_bd
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES,obtener_sesion

usuarios_bd = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    },
    "jose": {
        "username": "jose",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


router = APIRouter(
    prefix="/auth",
    tags=["AUTH"],
)



@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
    sesion = Depends(obtener_sesion)
) -> Token:
    print(form_data.username,form_data.password)
    usuarios_bd = await obtener_usuarios_bd(sesion)
    print("Usuarios",usuarios_bd)
    print("Tipo",type(usuarios_bd))
    user = authenticate_user(usuarios_bd, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]