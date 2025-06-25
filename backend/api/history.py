from fastapi import APIRouter
from database_manager import DatabaseManager
from typing import List

router = APIRouter()
db = DatabaseManager()

@router.get("/history", response_model=List[dict])
def get_history():
    """Récupère l'historique des comparaisons"""
    return db.get_comparison_history()
