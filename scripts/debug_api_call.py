from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
r = client.post('/api/adjudicate', json={'query':'Is AI consciousness morally relevant?','seed_vault':{}})
print('status_code=', r.status_code)
print('response_text=', r.text)
print('response_json=', r.json())
