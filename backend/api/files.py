from fastapi import APIRouter, UploadFile, File, HTTPException
from database_manager import DatabaseManager
from models import ReferenceFile
from typing import List
import shutil
import os

router = APIRouter()
db = DatabaseManager()

@router.get("/reference-files", response_model=List[dict])
def list_reference_files():
    """Liste tous les fichiers de référence actifs"""
    return db.get_reference_files()

@router.post("/reference-files")
def add_reference_file(file: UploadFile = File(...)):
    """Ajoute un nouveau fichier de référence"""
    try:
        # Sauvegarder le fichier sur le disque
        upload_dir = db.config.get_reference_files_dir()
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Ajouter à la BDD
        file_data = {
            'name': file.filename,
            'original_name': file.filename,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'mime_type': file.content_type,
            'row_count': 0,
            'column_count': 0,
            'description': '',
            'tags': '',
            'checksum': '',
        }
        db.add_reference_file(file_data)
        return {"success": True, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reference-files/{file_id}")
def delete_reference_file(file_id: int):
    """Supprime (désactive) un fichier de référence"""
    try:
        db.delete_reference_file(file_id)
        return {"success": True, "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
