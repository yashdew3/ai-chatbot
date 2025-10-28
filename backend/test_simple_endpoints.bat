@echo off
echo Testing Simple Backend Connection...
echo =====================================

echo.
echo 1. Testing Health Endpoint...
python -c "import requests; response = requests.get('http://127.0.0.1:8000/test'); print('Status:', response.status_code); print('Response:', response.json() if response.status_code == 200 else 'Failed')"

echo.
echo 2. Testing Sources Endpoint...
python -c "import requests; response = requests.get('http://127.0.0.1:8000/api/v1/data/sources'); print('Status:', response.status_code); sources = response.json().get('sources', []) if response.status_code == 200 else []; print(f'Found {len(sources)} sources'); [print(f'  - {s[\"name\"]}') for s in sources[:3]]"

echo.
echo 3. Testing Chat Endpoint (Simple Question)...
python -c "import requests; response = requests.post('http://127.0.0.1:8000/api/v1/chat', json={'question': 'Hello'}); print('Status:', response.status_code); print('Response:', response.json().get('answer', 'No answer')[:100] + '...' if response.status_code == 200 else 'Failed')"

echo.
echo 4. Testing Chat Endpoint (Document Question)...
python -c "import requests; response = requests.post('http://127.0.0.1:8000/api/v1/chat', json={'question': 'What is cloud computing?'}); print('Status:', response.status_code); print('Response:', response.json().get('answer', 'No answer')[:200] + '...' if response.status_code == 200 else 'Failed')"

echo.
echo Testing Complete!
pause