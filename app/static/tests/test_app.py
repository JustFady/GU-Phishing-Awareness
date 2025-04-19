import os
import json
import pytest

from app import app

LOG_FILE = 'logs/visits.json'


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a clean temp directory so tests don’t touch real logs
    workdir = tmp_path / "work"
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    # GET / should return 200 OK
    assert client.get('/').status_code == 200


def test_success_page_loads(client):
    # GET /success should return 200 OK
    assert client.get('/success').status_code == 200


def test_submit_creates_log(client):
    # POST /submit must create the log file
    client.post('/submit', data={'email': 'a@b.com'})
    assert os.path.isfile(LOG_FILE)


def test_log_not_empty(client):
    # Log file should have content after a submit
    client.post('/submit', data={'email': 'x@y.com'})
    assert os.path.getsize(LOG_FILE) > 0


def test_log_contains_email(client):
    # Last entry in log should match the submitted email
    email = 'test@domain.com'
    client.post('/submit', data={'email': email})
    data = json.load(open(LOG_FILE))
    assert data[-1]['email'] == email
