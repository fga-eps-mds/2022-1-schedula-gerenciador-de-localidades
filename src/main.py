from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import city, workstation
from utils.auth_utils import get_authorization

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

    if method == 'DELETE':
        if 'workstation' in url or 'city' in url:
            if auth != 'admin':
                return response_unauthorized
    if method == 'PUT':
        if 'workstation' in url or 'city' in url:
            if auth not in ['admin', 'manager']:
                return response_unauthorized
    if method == 'POST':
        if 'workstation' in url or 'city' in url:
            if auth not in ['admin', 'manager']:
                return response_unauthorized
    if method == 'GET':
        if 'workstation' in url or 'city' in url:
            if auth not in ['admin', 'manager', 'basic', 'public']:
                return response_unauthorized

    return await call_next(request)

app.include_router(workstation.router)
app.include_router(city.router)


@app.get("/")
def root():
    return {"APP": "Gerenciador de localidades is running"}
