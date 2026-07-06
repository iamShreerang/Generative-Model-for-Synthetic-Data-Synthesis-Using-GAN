$env:API_URL="http://localhost:8000"
$env:PYTHONPATH="."
Start-Process powershell -ArgumentList "-NoExit -Command `"C:\v\Scripts\Activate.ps1; uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload`""
Start-Process powershell -ArgumentList "-NoExit -Command `"C:\v\Scripts\Activate.ps1; streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0`""
Start-Sleep -Seconds 5
Start-Process "http://localhost:8501"
