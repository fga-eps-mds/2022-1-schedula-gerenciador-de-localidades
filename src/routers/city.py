from typing import Union
from unicodedata import name

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
    city_id: Union[int, None] = None, db: Session = Depends(get_db)
):
    try:
        if city_id:
            city = (
                db.query(City).filter_by(id=city_id).one_or_none()
            )

            if city is not None:
                city = jsonable_encoder(city)
                message = "Dados buscados com sucesso"
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
            all_data = db.query(City).all()
            all_data = [jsonable_encoder(c) for c in all_data]
            response_data = {
                "message": "Dados buscados com sucesso",
                "error": None,
                "data": all_data,
            }
            return JSONResponse(
                content=dict(response_data), status_code=status.HTTP_200_OK
            )

    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put("/city/{city_id}", tags=["City"])
async def update_city(
    data: CityModel,
    city_id: int = Path(title="The ID of the item to update"),
    db: Session = Depends(get_db),
):
    try:
        city = (
            db.query(City).filter_by(id=city_id).update(data.dict())
        )
        if city:
            db.commit()
            city_data = db.query(City).filter_by(id=city_id).one_or_none()
            city_data = jsonable_encoder(city_data)
            # data = jsonable_encoder(city)
            response_data = jsonable_encoder(
                {
                    "message": "Dado atualizado com sucesso",
                    "error": None,
                    "data": city_data,
                }
            )

            return JSONResponse(
                content=response_data, status_code=status.HTTP_200_OK
            )
        else:
            response_data = jsonable_encoder(
                {
                    "message": "Cidade não encontrada",
                    "error": None,
                    "data": None,
                }
            )

            return JSONResponse(
                content=response_data, status_code=status.HTTP_200_OK
            )
    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/city/{city_id}", tags=["City"])
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    try:
        city = db.query(City).filter_by(id=city_id).one_or_none()
        if city:
            db.query(City).filter_by(id=city_id).delete()
            db.commit()
            message = f"Cidade de id = {city_id} deletada com sucesso"

        else:
            message = f"Cidade de id = {city_id} não encontrada"

        response_data = {"message": message, "error": None, "data": None}

        return JSONResponse(
            content=response_data, status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content=get_error_response(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
