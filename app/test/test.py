from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
# Configuración de Seguridad
SECRET_KEY = "credencial_prueba_para_desarrollo_no_usar_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de Passlib para usar bcrypt en el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define de dónde obtendrá FastAPI el token (en este caso, la ruta /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

