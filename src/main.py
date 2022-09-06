import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    if 'workstation' in str(request.url):
        if method == 'DELETE':
            if auth != 'admin':
                return response_unauthorized
        elif method in ['PUT','POST']:
            if auth not in ['admin','manager']:
                return response_unauthorized
        elif method =='GET':
            if auth not in ['admin','manager','basic']:
                return response_unauthorized
    return await call_next                       

app.include_router(workstation.router)
app.include_router(city.router)

@app.get("/")
def root():
    return {"APP": "Gerenciador de localidades is running"}
