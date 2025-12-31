import io
import os
from pathlib import Path
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    r = client.get('/api/health')
    assert r.status_code == 200
    payload = r.json()
    assert payload.get('status') == 'healthy'


def test_adjudicate_endpoint():
    r = client.post('/api/adjudicate', json={"query": "Is AI consciousness morally relevant?", "seed_vault": {}})
    assert r.status_code == 200
    data = r.json()
    assert 'verdict' in data
    assert data.get('deliberation_complete') is True


def test_upload_endpoint_and_cleanup():
    # Create a small in-memory text file
    file_content = b"Hello UCM uploads"
    files = [("files", ("test_upload.txt", io.BytesIO(file_content), "text/plain"))]

    r = client.post('/api/upload', files=files)
    assert r.status_code == 200
    data = r.json()
    assert 'files' in data and len(data['files']) == 1

    uploaded_name = data['files'][0]['filename']
    # Uploaded files are stored in repo_root/uploads
    repo_root = Path(__file__).resolve().parents[2]
    uploaded_path = repo_root / 'uploads' / uploaded_name
    assert uploaded_path.exists()

    # Clean up
    try:
        uploaded_path.unlink()
    except Exception:
        pass
