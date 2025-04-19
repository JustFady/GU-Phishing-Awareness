import os
import json
import pytest

from app import app

LOG_FILE = 'logs/visits.json'


def test_homepage_loads():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200


def test_submit_saves_email_and_creates_file():
    client = app.test_client()

    # clean up any existing file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # submit one email
    resp = client.post('/submit', data={'email': 'simple@test.com'})
    assert resp.status_code == 302

    # the file should now exist
    assert os.path.exists(LOG_FILE)

    # and contain a JSON list with our email
    data = json.load(open(LOG_FILE))
    assert isinstance(data, list)
    assert data[-1]['email'] == 'simple@test.com'


def test_success_page_loads():
    client = app.test_client()
    res = client.get('/success')
    assert res.status_code == 200
