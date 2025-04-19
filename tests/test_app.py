import os
import json
from app.app import app

LOG_FILE = 'logs/visits.json'

def testHomepageStatusCode():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200

def testSuccessStatusCode():
    client = app.test_client()
    res = client.get('/success')
    assert res.status_code == 200

def testSubmitRedirects():
    client = app.test_client()
    res = client.post('/submit', data={'email': 'a@b.com'})
    assert res.status_code == 302

def testLogFileCreated():
    client = app.test_client()
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    client.post('/submit', data={'email': 'x@y.com'})
    assert os.path.exists(LOG_FILE)

def testLogFileNotEmpty():
    client = app.test_client()
    client.post('/submit', data={'email': 'notempty@test.com'})
    assert os.path.getsize(LOG_FILE) > 0

def testLoggedDataIsJson():
    with open(LOG_FILE) as f:
        data = json.load(f)
    assert isinstance(data, list)

def testEmailFieldLogged():
    client = app.test_client()
    client.post('/submit', data={'email': 'fieldcheck@test.com'})
    with open(LOG_FILE) as f:
        data = json.load(f)
    assert 'email' in data[-1]

def testLoggedEmailValue():
    email = 'testemail@gu.edu'
    client = app.test_client()
    client.post('/submit', data={'email': email})
    with open(LOG_FILE) as f:
        data = json.load(f)
    assert data[-1]['email'] == email

def testLogEntryHasIp():
    with open(LOG_FILE) as f:
        data = json.load(f)
    assert 'ip' in data[-1]

def testLogEntryHasUserAgent():
    with open(LOG_FILE) as f:
        data = json.load(f)
    assert 'user_agent' in data[-1]
