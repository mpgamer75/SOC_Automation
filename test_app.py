import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirection vers /upload

def test_upload_page(client):
    response = client.get('/upload')
    assert response.status_code == 200
    assert b"Upload Excel File" in response.data
