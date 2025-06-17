import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de l'application"""
    
    # Configuration du serveur
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuration CORS - Compatible avec l'ancienne structure
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', f'{FRONTEND_URL},http://127.0.0.1:3000').split(',')
    
    # Configuration des fichiers - Compatible avec l'ancienne structure
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB par défaut
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'csv,xlsx,xls').split(',')
    SUPPORTED_FORMATS = [f'.{ext}' for ext in ALLOWED_EXTENSIONS]
    
    # Configuration de sécurité
    SECRET_KEY = os.getenv('SECRET_KEY', 'altice-file-comparator-default-key-change-in-production')
    
    # Configuration des logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Configuration de la base de données (pour future utilisation)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./file_comparator.db')
    
    # Configuration pour Supabase (futur)
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Configuration de l'environnement
    ENV = os.getenv('ENV', 'production')
    
    @classmethod
    def is_production(cls):
        """Vérifie si l'application est en mode production"""
        return cls.ENV.lower() == 'production' or not cls.DEBUG
    
    @classmethod
    def get_cors_origins(cls):
        """Retourne les origines CORS configurées"""
        origins = cls.ALLOWED_ORIGINS.copy()
        if cls.FRONTEND_URL not in origins:
            origins.append(cls.FRONTEND_URL)
        return origins 