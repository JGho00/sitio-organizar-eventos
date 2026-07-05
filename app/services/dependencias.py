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



