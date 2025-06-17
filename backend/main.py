from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from file_comparator import FileComparator
from config import Config
import os
from dotenv import load_dotenv
import logging

# Configuration des logs
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Altice File Comparator API",
    description="API para comparar archivos CSV, Excel y XLS",
    version="1.0.0",
    debug=Config.DEBUG
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia del comparador
comparator = FileComparator()

@app.get("/")
async def root():
    """
    Endpoint de prueba para verificar que la API está funcionando
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
    Endpoint de salud para monitoreo
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
        JSON con el resultado de la comparación
    """
    
    # Validar tipos de archivo
    allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    def validate_file(file: UploadFile) -> bool:
        if not file.filename:
            return False
        extension = file.filename.lower().split('.')[-1]
        return extension in allowed_extensions
    
    if not validate_file(file1):
        raise HTTPException(
            status_code=400, 
            detail=f"Archivo de referencia no válido. Formatos permitidos: {', '.join(allowed_extensions)}"
        )
    
    if not validate_file(file2):
        raise HTTPException(
            status_code=400, 
            detail=f"Archivo a comparar no válido. Formatos permitidos: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Leer contenido de los archivos
        file1_content = await file1.read()
        file2_content = await file2.read()
        
        # Validar tamaño de archivos
        if len(file1_content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo de referencia es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        if len(file2_content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo a comparar es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        # Validar que los archivos no estén vacíos
        if len(file1_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo de referencia está vacío")
        
        if len(file2_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo a comparar está vacío")
        
        logger.info(f"Comparando archivos: {file1.filename} vs {file2.filename}")
        
        # Realizar la comparación
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
    """
    try:
        # Validar extensión
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nombre de archivo no válido")
        
        extension = file.filename.lower().split('.')[-1]
        if extension not in Config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado: {extension}"
            )
        
        # Leer y validar contenido
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        if len(content) > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"El archivo es demasiado grande. Máximo: {Config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB"
            )
        
        # Intentar leer el archivo
        df = comparator.read_file(content, file.filename)
        
        return {
            "valid": True,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()[:10],  # Primeras 10 columnas
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
    logger.info(f"Démarrage du serveur sur {Config.API_HOST}:{Config.API_PORT}")
    logger.info(f"Environnement: {Config.ENV}")
    logger.info(f"Frontend URL: {Config.FRONTEND_URL}")
    uvicorn.run(
        app, 
        host=Config.API_HOST, 
        port=Config.API_PORT,
        log_level=Config.LOG_LEVEL.lower()
    )