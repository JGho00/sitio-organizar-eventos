import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.ERROR)

    # Crea un archivo log que rota automáticamente cada medianoche
    handler = TimedRotatingFileHandler(
        "app_errors.log", 
        when="midnight", 
        interval=1, 
        backupCount=30 # Conserva 30 días de historial
    )
    
    # Formato profesional: Tiempo - Nombre del Logger - Nivel - Mensaje
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logging()