import os
import pytest
from main import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    db.create_all()

    yield client

def cleanup():
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get("/")
    assert b'Enter your name' in response.data


def test_fail_index_not_logged_in(client):
    response = client.get('/')
    assert b'enter you Name' in response.data


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test", "user-email": "test@gmail.com",
                                "user-password":"password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'Enter your guess' in response.data

