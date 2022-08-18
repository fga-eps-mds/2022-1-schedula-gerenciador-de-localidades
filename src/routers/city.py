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


def get_error_response(e: Exception):
    return {
        "message": "Erro ao processar dados",
        "error": str(e),
        "data": None,
    }


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


@router.get("/city", tags=["City"])
async def get_city(
    city_id: Union[int, None] = None,
    db: Session = Depends(get_db),
    workstation_id: Union[int, None] = None,
):
    try:
        if city_id:
            city = db.query(City).filter_by(id=city_id).one_or_none()
            if city:
                city = jsonable_encoder(city)
                message = "Dados buscados com exito"
                status_code = status.HTTP_200_OK
            else:
                message = "Nenhuma cidade encontrada"
                status_code = status.HTTP_200_OK

            response_data = {
                "message": message,
                "error": None,
                "data": city,
            }
            return JSONResponse(
                content=jsonable_encoder(response_data),
                status_code=status_code,
            )

        else:
            if workstation_id:
                all_data = (
                    db.query(City)
                    .filter_by(workstation_id=workstation_id, active=True)
                    .all()
                )
            else:
                all_data = db.query(City).filter_by(active=True).all()
            all_data = [jsonable_encoder(c) for c in all_data]

            response_data = {
                "message": "Dados buscados com sucesso",
                "error": None,
                "data": all_data,
            }
            return JSONResponse(
                content=response_data, status_code=status.HTTP_200_OK
            )
    except Exception as e:
        response_data = {
            "message": "Erro ao buscar dados",
            "error": str(e),
            "data": None,
        }
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
