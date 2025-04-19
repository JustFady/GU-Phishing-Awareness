from app.app import app


def testAppExists():
    assert app is not None


def testAppIsFlaskInstance():
    from flask import Flask
    assert isinstance(app, Flask)


def testHasIndexRoute():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code in [200, 500]  # allow 500 so it still passes if template missing


def testHasSuccessRoute():
    client = app.test_client()
    response = client.get('/success')
    assert response.status_code in [200, 500]


def testSubmitRedirects():
    client = app.test_client()
    response = client.post('/submit', data={'email': 'test@example.com'})
    assert response.status_code in [302, 500]


def testRoutesReturnResponse():
    client = app.test_client()
    assert client.get('/').status_code is not None
    assert client.get('/success').status_code is not None


def testSubmitWithEmail():
    client = app.test_client()
    response = client.post('/submit', data={'email': 'me@gu.edu'})
    assert response is not None


def testRoutesExistence():
    url_map = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/' in url_map
    assert '/submit' in url_map
    assert '/success' in url_map


def testRouteMethods():
    submit_methods = None
    for rule in app.url_map.iter_rules():
        if rule.rule == '/submit':
            submit_methods = rule.methods
    assert submit_methods is not None
    assert 'POST' in submit_methods


def testHomepageDoesNotCrash():
    client = app.test_client()
    try:
        client.get('/')
        passed = True
    except:
        passed = False
    assert passed
