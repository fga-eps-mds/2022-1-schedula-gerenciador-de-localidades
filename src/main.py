import time
from fastapi import FastAPI, Request
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

@app.middleware("http")
async def process_request_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process time"] = str(process_time)
    return response

app.include_router(workstation.router)
app.include_router(city.router)

@app.get("/")
def root():
    return {"APP": "Gerenciador de localidades is running"}
