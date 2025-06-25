from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from file_comparator import FileComparator
from config import Config
import os
from dotenv import load_dotenv
import logging
from api import files_router, comparisons_router, history_router

# Configuracion del sistema de logs
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde archivo .env
load_dotenv()

app = FastAPI(
    title="Altice File Comparator API",
    description="API para comparar archivos CSV, Excel y XLS",
    version="1.0.0",
    debug=Config.DEBUG
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del comparador de archivos
comparator = FileComparator()

app.include_router(files_router)
app.include_router(comparisons_router)
app.include_router(history_router)

@app.get("/")
async def root():
    """
    Endpoint de prueba para verificar que la API está funcionando correctamente
    """
    return {
        "message": "Altice File Comparator API está funcionando",
        "version": "1.0.0",
        "environment": Config.ENV,
        "supported_formats": Config.SUPPORTED_FORMATS,
        "max_file_size": f"{Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB",
        "frontend_url": Config.FRONTEND_URL
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de salud para monitoreo del servicio
    """
    return {
        "status": "healthy", 
        "service": "file-comparator",
        "environment": Config.ENV,
        "version": "1.0.0"
    }

@app.post("/compare")
async def compare_files(
    file1: UploadFile = File(..., description="Archivo de referencia"),
    file2: UploadFile = File(..., description="Archivo a comparar")
):
    """
    Endpoint principal para comparar dos archivos
    
    Args:
        file1: Archivo de referencia (CSV, XLSX, XLS)
        file2: Archivo a comparar (CSV, XLSX, XLS)
    
    Returns:
        JSON con el resultado detallado de la comparación
    """
    
    # Validar tipos de archivo permitidos
    allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    def validate_file(file: UploadFile) -> bool:
        if not file.filename:
            return False
        extension = file.filename.lower().split('.')[-1]
        return extension in allowed_extensions
    
    # Validar archivo de referencia
    if not validate_file(file1):
        raise HTTPException(
            status_code=400, 
            detail=f"Archivo de referencia no válido. Formatos permitidos: {', '.join(allowed_extensions)}"
        )
    
    # Validar archivo a comparar
    if not validate_file(file2):
        raise HTTPException(
            status_code=400, 
            detail=f"Archivo a comparar no válido. Formatos permitidos: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Leer contenido de los archivos en memoria
        file1_content = await file1.read()
        file2_content = await file2.read()
        
        # Validar tamaño del archivo de referencia
        if len(file1_content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo de referencia es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        # Validar tamaño del archivo a comparar
        if len(file2_content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo a comparar es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        # Verificar que los archivos no estén vacíos
        if len(file1_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo de referencia está vacío")
        
        if len(file2_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo a comparar está vacío")
        
        logger.info(f"Comparando archivos: {file1.filename} vs {file2.filename}")
        
        # Ejecutar la comparación usando el motor de comparación
        result = comparator.compare_files(
            file1_content, file1.filename,
            file2_content, file2.filename
        )
        
        logger.info(f"Comparación completada: {result['summary']['differences']} diferencias encontradas")
        
        return JSONResponse(content=result)
        
    except ValueError as ve:
        logger.error(f"Error de validación: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/validate-file")
async def validate_file_endpoint(file: UploadFile = File(...)):
    """
    Endpoint para validar un archivo antes de la comparación
    Verifica formato, tamaño y contenido del archivo
    """
    try:
        # Validar que el archivo tenga nombre
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nombre de archivo no válido")
        
        # Verificar extensión del archivo
        extension = file.filename.lower().split('.')[-1]
        if extension not in Config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado: {extension}"
            )
        
        # Leer y validar contenido del archivo
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        # Verificar tamaño del archivo
        if len(content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        # Intentar leer el archivo para verificar que sea válido
        df = comparator.read_file(content, file.filename)
        
        return {
            "valid": True,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()[:10],  # Mostrar solo las primeras 10 columnas
            "size_bytes": len(content)
        }
        
    except Exception as e:
        logger.error(f"Error validando archivo {file.filename}: {str(e)}")
        return {
            "valid": False,
            "error": str(e),
            "filename": file.filename if file.filename else "unknown"
        }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Iniciando servidor en {Config.API_HOST}:{Config.API_PORT}")
    logger.info(f"Ambiente: {Config.ENV}")
    logger.info(f"URL del Frontend: {Config.FRONTEND_URL}")
    uvicorn.run(
        app, 
        host=Config.API_HOST, 
        port=Config.API_PORT,
        log_level=Config.LOG_LEVEL.lower()
    ) 