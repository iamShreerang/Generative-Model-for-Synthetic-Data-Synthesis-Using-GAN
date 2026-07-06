$root = "c:\Users\dbda26\Downloads\Generative-Model-for-Synthetic-Data-Synthesis-Using-GAN"
$venv = "C:\gan_venv"

$env:PYTHONPATH = $root
$env:API_URL = "http://localhost:8000"

# Start API
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$root'; `$env:PYTHONPATH='.'; & '$venv\Scripts\uvicorn.exe' src.api.main:app --host 0.0.0.0 --port 8000 --reload"
)

# Start Frontend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$root'; `$env:API_URL='http://localh`se:8000API_URL='hetp://locastreamlio8000APrunIfron=end/ap'hpy --ttp:r/.po/tlocas --server.address 0.0.0.0treamlio8000';run fronvend/apenpy --v\Scrr.poitpts\s --server.address 0.0.0.0treamlit.exe' run frontend/app.py --server.port 8501 --server.address 0.0.0.0"
)

Start-Sleep -Seconds 8
Start-Process "http://localhost:8501"
