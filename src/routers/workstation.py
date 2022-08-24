from typing import Dict, List, Union

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from database import engine, get_db
from models import Base, City, Workstation, Phone

router = APIRouter()


class WorkstationModel(BaseModel):
    name: str
    asdl_vpn: bool = False
    link: str | None = None
    ip: str | None = None
    regional: bool = False
    city_id: int
    regional_id: int | None = None
    active: bool = True
    phone: List[Dict[str, str]] | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "2ª DRP - Aparecida",
                "asdl_vpn": True,
                "link": "7ª DP  Aparecida",
                "ip": "10.11.1.1",
                "regional": True,
                "city_id": 1,
                "phone": [{"phone": "48946513"}, {"phone": "161651561"}]
            }
        }

    Base.metadata.create_all(bind=engine)


@router.post(
    "/workstation", tags=["Workstation"], response_model=WorkstationModel
)
async def post_workstation(
    data: WorkstationModel, db: Session = Depends(get_db)
):
    data.name = data.name.strip()
    try:
        if not data.regional and not data.regional_id:
            return JSONResponse(
                content={
                    "message": "Erro ao processar dados",
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not db.query(City).filter_by(id=data.city_id).one_or_none():
            return JSONResponse(
                content={
                    "message": f"A cidade de id {data.city_id} não está cadastrada.",  # noqa E501
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        new_phones = [Phone(**p) for p in data.phone]
        new_object = Workstation(**data.dict())
        new_object.phone = new_phones
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        new_object = jsonable_encoder(new_object)
        response_data = jsonable_encoder(
            {
                "message": "Dado cadastrado com sucesso",
                "error": None,
                "data": new_object,
            }
        )

        return JSONResponse(
            content=response_data, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/workstation", tags=["Workstation"])
def get_workstation(
    id: Union[int, None] = None, db: Session = Depends(get_db)
):

    try:
        if id:
            workstation = (
                db.query(Workstation)
                .filter(Workstation.id == id)
                .one_or_none()
            )

            if workstation is None:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": "Dados não encontrados",
                        "error": None,
                        "data": None,
                    },
                )

            else:
                workstation = jsonable_encoder(workstation)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": "Dados buscados com sucesso",
                        "error": None,
                        "data": workstation,
                    },
                )

        else:
            all_data = db.query(Workstation).filter_by(active=True).all()
            all_data_json = jsonable_encoder(all_data)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "dados buscados com sucesso",
                    "error": None,
                    "data": all_data_json,
                },
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Erro ao obter dados",
                "error": str(e),
                "data": None,
            },
        )


@router.delete(
    "/workstation/{workstation_id}",
    tags=["Workstation"],
    response_model=WorkstationModel,
)
async def delete_workstation(
    workstation_id: int, db: Session = Depends(get_db)
):
    try:
        workstation: WorkstationModel = db.query(Workstation).filter_by(
            id=workstation_id
        ).one_or_none()
        if not workstation:
            return JSONResponse(
                content={
                    "message": f"Nenhum posto de trabalho com id = {workstation_id} encontrado.",  # noqa E501
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        workstation.active = False
        db.add(workstation)
        db.commit()
        return JSONResponse(
            content={
                "message": f"Posto de trabalho de id = {workstation_id} deletado com sucesso",  # noqa E501
                "error": True,
                "data": None,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return JSONResponse(
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put(
    "/workstation/{workstation_id}",
    tags=["Workstation"],
    response_model=WorkstationModel,
)
async def put_workstation(
    workstation_id: int, data: WorkstationModel, db: Session = Depends(get_db)
):
    try:
        if data.name:
            data.name = data.name.strip()
        if not data.regional and not data.regional_id:
            return JSONResponse(
                content={
                    "message": "Caso o posto de trabalho não seja regional, forneça o a regional à qual ele pertence.",  # noqa E501
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not db.query(City).filter_by(id=data.city_id).one_or_none():
            return JSONResponse(
                content={
                    "message": f"A cidade de id = {data.city_id} não está cadastrada.",  # noqa E501
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if (
            not db.query(Workstation)
            .filter_by(id=workstation_id)
            .one_or_none()
        ):
            return JSONResponse(
                content={
                    "message": f"O Posto de Trabalho de id = {workstation_id} não está cadastrado.",  # noqa E501
                    "error": True,
                    "data": None,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        db.query(Workstation).filter_by(id=workstation_id).update(data.dict())
        db.commit()

        response_data = jsonable_encoder(
            {
                "message": "Dado atualizado com sucesso",
                "error": None,
                "data": jsonable_encoder(data),
            }
        )
        return JSONResponse(
            content=response_data, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
