import os
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel,create_engine,Session
from typing import Generator
from dotenv import load_dotenv

load_dotenv()
POSTGRES_SERVER =os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
url:str = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

engine = create_engine(
    url,
    pool_pre_ping=True,  # Verifica que la conexión siga viva antes de usarla
    pool_size=10,        # Número máximo de conexiones simultáneas persistentes
    max_overflow=20      # Conexiones extra permitidas en picos de tráfico
    #engine = create_engine(url)
    #return engine
    )

def obtener_sesion() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
