from typing import Union

from fastapi import APIRouter, Depends, Path, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, City

router = APIRouter()


class CityModel(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Cidade",
            }
        }


Base.metadata.create_all(bind=engine)


@router.post("/city", tags=["City"], response_model=CityModel)
async def post_city(data: CityModel, db: Session = Depends(get_db)):
    try:
        city = City(**data.dict())

        db.add(city)
        db.commit()
        db.refresh(city)
        city = jsonable_encoder(city)
        response_data = jsonable_encoder(
            {
                "message": "Dados cadastrados com sucesso",
                "error": None,
                "data": city,
            }
        )

        return JSONResponse(
            content=response_data, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        response_data = jsonable_encoder(
            {
                "message": "Erro ao cadastrar os dados",
                "error": str(e),
                "data": None,
            }
        )

        return JSONResponse(
            content=response_data,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
