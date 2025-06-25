from fastapi import APIRouter, HTTPException
from database_manager import DatabaseManager
from typing import List

router = APIRouter()
db = DatabaseManager()

@router.get("/comparisons", response_model=List[dict])
def list_comparisons():
    """Liste l'historique des comparaisons"""
    return db.get_comparison_history()

@router.get("/comparisons/{comparison_id}")
def get_comparison(comparison_id: int):
    """Détail d'une comparaison"""
    result = db.get_comparison_details(comparison_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comparaison non trouvée")
    return result

@router.delete("/comparisons/{comparison_id}")
def delete_comparison(comparison_id: int):
    """Supprime une comparaison de l'historique"""
    try:
        db.delete_comparison(comparison_id)
        return {"success": True, "comparison_id": comparison_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
