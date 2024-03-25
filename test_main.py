# FILEPATH: /Users/amal/development/hardware/record audio/record/test_main.py
import pytest
from main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup(client):
    # Mock data
    data = {
        "name": "test",
        "password": "test",
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post('/signup', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200

def test_record(client):
    response = client.post('/record')
    assert response.status_code == 200
    assert response.data == b"Completed"

def test_predictLungs(client):
    response = client.post('/predictLungs')
    assert response.status_code == 200

def test_predictHeart(client):
    response = client.post('/predictHeart')
    assert response.status_code == 200

def test_download(client):
    response = client.get('/download')
    assert response.status_code == 200