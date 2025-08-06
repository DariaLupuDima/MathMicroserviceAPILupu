# test_api.py

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_factorial_api(client):
    response = client.post('/factorial', json={"n": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 120

def test_power_api(client):
    response = client.post('/pow', json={"a": 2, "b": 4})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 16

def test_fibonacci_api(client):
    response = client.post('/fibonacci', json={"n": 7})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 13

def test_factorial_missing_input(client):
    response = client.post('/factorial', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_factorial_negative_number(client):
    response = client.post('/factorial', json={"n": -3})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_power_invalid_input(client):
    response = client.post('/pow', json={"a": "apple", "b": 2})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_fibonacci_missing_input(client):
    response = client.post('/fibonacci', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
