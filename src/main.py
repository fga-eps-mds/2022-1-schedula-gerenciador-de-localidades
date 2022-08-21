from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import city, workstation

app = FastAPI()

app.include_router(workstation.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(city.router)


@app.get("/")
def root():
    return {"APP": "Gerenciador de localidades is running"}
