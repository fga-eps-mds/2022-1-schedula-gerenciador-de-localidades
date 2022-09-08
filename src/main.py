import time
import os
from typing import Any, List, Union

from passlib.context import CryptContext
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.auth_utils import get_authorization
from routers import city, workstation
                 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

response_unauthorized = JSONResponse({
    "message": "Acesso negado",
    "error": True,
    "data": None,
}, status.HTTP_401_UNAUTHORIZED)

@app.middleware("http")
async def process_request_headers(request: Request, call_next):
    auth = str(get_authorization(request))
    method = str(request.method)
    url = str(request.url)

    if 'workstation' in url or 'cidades' in url:
        if method == 'DELETE':
            if auth != 'admin':
                return response_unauthorized
        if method == 'PUT'or method == 'POST':
            if auth not in ['admin','manager']:
                return response_unauthorized
        if method =='GET':
            if auth not in ['admin','manager','basic','public']:
                return response_unauthorized
    return await call_next(request)

app.include_router(workstation.router)
app.include_router(city.router)

@app.get("/")
def root():
    return {"APP": "Gerenciador de localidades is running"}

response_unauthorized = JSONResponse({
    "message": "Acesso negado",
    "error": True,
    "data": None, 
}, status.HTTP_401_UNAUTHORIZED)