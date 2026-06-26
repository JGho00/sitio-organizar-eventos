from sqlmodel import SQLModel,Session,select
from fastapi import Depends,HTTPException,status
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer

from models.model_usuario import Usuario
from core.config import oauth2_scheme
from core.config import SECRET_KEY,ALGORITHM
from pydantic import BaseModel
from core.config import obtener_sesion

import jwt
from jwt.exceptions import InvalidTokenError


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


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




     
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(usuarios = obtener_usuarios_bd(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user




def get_user(db_user, username: str):
    usuario = None
    
    for user in db_user:
        if user.username == username:
            usuario = user
    return usuario


def authenticate_user(user_bd, username: str, password: str):
    user:Usuario = get_user(user_bd, username)
    print(f"User {user} tipó {type(user)}")
    if not user:
        return False
    print(f"User correcto")
    if user.password_hash != password:
        print(f"Pass incorrecta")
        return False
    print(f"Ingresé")
    
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire:datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt:jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f'TOKEN\n{encoded_jwt}')
    return encoded_jwt



async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
