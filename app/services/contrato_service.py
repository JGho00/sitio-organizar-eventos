from io import BytesIO
import pandas as pd
from fastapi import UploadFile
async def decodificar_archivo_egresados(archivo:UploadFile):
    contenido = await archivo.read()
    archivo_pandas:BytesIO = BytesIO(contenido)
    return archivo_pandas

def obtener_df_egresados(archivo_bytes:BytesIO):
    df:pd.DataFrame = pd.read_excel(archivo_bytes)
    return df