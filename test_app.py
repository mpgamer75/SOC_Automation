import os
import pytest
from io import BytesIO
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test de la page d'index"""
    response = client.get('/')
    assert response.status_code == 302  # Redirection vers /upload
    assert response.location == 'http://localhost/upload'

def test_upload_page(client):
    """Test de la page d'upload"""
    response = client.get('/upload')
    assert response.status_code == 200
    assert b"Upload Excel File" in response.data

def test_upload_valid_file(client):
    """Test de l'upload d'un fichier Excel valide"""
    data = {
        'file': (BytesIO(b'Nom Complet\nJohn Doe\nJane Smith\n'), 'test.xlsx')
    }
    response = client.post('/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Résultats de la comparaison".encode('utf-8') in response.data

def test_upload_invalid_file(client):
    """Test de l'upload d'un fichier Excel invalide"""
    data = {
        'file': (BytesIO(b'Invalid Content'), 'invalid.xlsx')
    }
    response = client.post('/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Erreur lors de la lecture du fichier Excel" in response.data

def test_compare_excel_to_ad(client):
    """Test de la fonction compare_excel_to_ad"""
    from app import compare_excel_to_ad
    # Cas avec un fichier Excel valide
    valid_file = BytesIO(b'Nom Complet\nJohn Doe\nJane Smith\n')
    error, results = compare_excel_to_ad(valid_file)
    assert error is None
    assert len(results) == 2

    # Cas avec un fichier Excel invalide
    invalid_file = BytesIO(b'Invalid Content')
    error, results = compare_excel_to_ad(invalid_file)
    assert error is not None
    assert len(results) == 0
