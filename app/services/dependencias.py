from io import BytesIO
import pandas as pd
from fastapi import UploadFile
from datetime import datetime

async def decodificar_archivo_egresados(archivo:UploadFile):
    contenido = await archivo.read()
    archivo_pandas:BytesIO = BytesIO(contenido)
    return archivo_pandas

def obtener_df_egresados(archivo_bytes:BytesIO):
    df:pd.DataFrame = pd.read_excel(archivo_bytes)
    return df

def obtener_fecha(fecha_str: str = None) -> dict:
    """
    Valida una fecha en formato 'mm-yyyy' (o toma la actual si es None/vacía)
    y retorna un diccionario con la fecha en diferentes formatos.
    """
    # Validar entrada
    if not fecha_str or str(fecha_str).strip() == "":
        fecha_obj = datetime.now()
    else:
        # 2. Validar y parsear el formato string "mm-yyyy"
        try:
            fecha_obj = datetime.strptime(fecha_str.strip(), "%m-%Y")
        except ValueError:
            raise ValueError("El formato de fecha debe ser 'mm-yyyy' (ejemplo: '07-2026').")

    formatos_fechas:dict = {
        "dd_mm_yyyy_hh_mm_ss": fecha_obj.strftime("%d_%m_%Y_%H_%M_%S"),
        "dd_mm_yyyy_hh_mm": fecha_obj.strftime("%d_%m_%Y_%H_%M"),
        "dd_mm_yyyy": fecha_obj.strftime("%d_%m_%Y"),
        "mm_yyyy": fecha_obj.strftime("%m_%Y")
    }

    return formatos_fechas




anios = {
        
        "2020": "2020",
        "2021": "2021",
        "2022": "2022",
        "2023": "2023",
        "2024": "2024",
        "2025": "2025",
        "2026": "2026",
        "2027": "2027",
        "2028": "2028",
    }


divisiones = {
        "1-A": "1° A",
        "1-B": "1° B",
        "1-C": "1° C",
        "1-D": "1° D",
        "1-E": "1° E",
        "1-F": "1° F",
}


interes_mora = {
    
        "1": "1%",
        "2": "2%",
        "3": "3%",
        "4": "4%",
        "5": "5%",
        "6": "6%",
        "7": "7%",
        "8": "8%",
        "9": "9%",
        "10": "10%",
        "11": "11%",
        "12": "12%",
        "13": "13%",
        "14": "14%",
        "15": "15%",
        "16": "16%",
        "17": "17%",
        "18": "18%",
        "19": "19%",
        "20": "20%"
}




