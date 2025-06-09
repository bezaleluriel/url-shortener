import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app, url_db

client = TestClient(app)

def test_shorten_and_redirect():
    response = client.post('/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 200
    data = response.json()
    assert 'code' in data
    code = data['code']
    assert code in url_db

    r = client.get(f'/{code}', allow_redirects=False)
    assert r.status_code == 307
    assert r.headers['location'] == 'https://example.com'

def test_redirect_not_found():
    r = client.get('/nonexistent', allow_redirects=False)
    assert r.status_code == 404
