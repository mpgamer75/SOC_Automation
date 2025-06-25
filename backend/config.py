import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

class Config:
    """Configuracion centralizada de la aplicacion"""
    
    # Configuracion del servidor API
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuracion CORS - Compatible con la estructura existente
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', f'{FRONTEND_URL},http://127.0.0.1:3000').split(',')
    
    # Configuracion de archivos - Compatible con la estructura existente
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB por defecto
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'csv,xlsx,xls').split(',')
    SUPPORTED_FORMATS = [f'.{ext}' for ext in ALLOWED_EXTENSIONS]
    
    # Configuracion de seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'altice-file-comparator-default-key-change-in-production')
    
    # Configuracion del sistema de logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Configuracion de base de datos (para uso futuro)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./file_comparator.db')
    
    # Configuracion para Supabase (futuro)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Configuracion del ambiente de ejecucion
    ENV = os.getenv('ENV', 'production')
    
    @classmethod
    def is_production(cls):
        """Verifica si la aplicacion esta ejecutandose en modo produccion"""
        return cls.ENV.lower() == 'production' or not cls.DEBUG
    
    @classmethod
    def get_cors_origins(cls):
        """Retorna las origenes CORS configuradas para el servidor"""
        origins = cls.ALLOWED_ORIGINS.copy()
        if cls.FRONTEND_URL not in origins:
            origins.append(cls.FRONTEND_URL)
        return origins 