import os

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
