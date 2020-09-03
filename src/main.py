import sys
import os
from fastapi import FastAPI
from uvicorn import run
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

settings = importlib.import_module('settings')

api = importlib.import_module('routers.api')

app = FastAPI()

app.include_router(api.router)

if __name__ == "__main__":
    run('main:app', host='0.0.0.0', port=5000, reload=True)
