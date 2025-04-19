import os
import json
import pytest
from app import app

# Path to the log file created by the app
LOG_FILE = 'logs/visits.json'

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary directory for logs
    workdir = tmp_path / "work"
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    # GET / should return 200 OK
    response = client.get('/')
    assert response.status_code == 200

def test_success_page_loads(client):
    # GET /success should return 200 OK
    response = client.get('/success')
    assert response.status_code == 200

def test_redirect_after_submit(client):
    # POST /submit should redirect (302)
    response = client.post('/submit', data={'email': 'test@example.com'})
    assert response.status_code == 302

def test_submit_creates_log_file(client):
    # After submitting, the log file must exist
    client.post('/submit', data={'email': 'log@file.com'})
    assert os.path.isfile(LOG_FILE)

def test_log_not_empty(client):
    # The log file should not be empty after a submit
    client.post('/submit', data={'email': 'a@b.com'})
    assert os.path.getsize(LOG_FILE) > 0

def test_log_is_list(client):
    # The JSON stored should be a list
    client.post('/submit', data={'email': 'list@val.com'})
    data = json.load(open(LOG_FILE))
    assert isinstance(data, list)

def test_log_contains_email(client):
    # The last entry in the log should match the submitted email
    email = 'hello@world.com'
    client.post('/submit', data={'email': email})
    data = json.load(open(LOG_FILE))
    assert data[-1]['email'] == email

def test_multiple_submissions(client):
    # Two submissions should result in two entries
    client.post('/submit', data={'email': 'one@a.com'})
    client.post('/submit', data={'email': 'two@b.com'})
    data = json.load(open(LOG_FILE))
    assert len(data) == 2

def test_time_and_ip_keys_exist(client):
    # Each log entry should have 'time' and 'ip' keys
    client.post('/submit', data={'email': 'ip@test.com'})
    entry = json.load(open(LOG_FILE))[-1]
    assert 'time' in entry and 'ip' in entry

def test_valid_json_format(client):
    # The log file must be valid JSON
    client.post('/submit', data={'email': 'json@test.com'})
    json.load(open(LOG_FILE))  # will raise if invalid
