from typing import Dict, List, Union

from fastapi import APIRouter, Depends, Path
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from database import engine, get_db
from models import Base, City, Phone, Workstation

router = APIRouter()

Base.metadata.create_all(bind=engine)


class WorkstationModel(BaseModel):
    name: str
    adsl_vpn: bool = False
    link: str | None = None
    ip: str | None = None
    regional: bool = False
    city_id: int
    regional_id: int | None = None
    active: bool = True
    phones: List[Dict[str, str]] | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "2ª DRP - Aparecida",
                "adsl_vpn": True,
                "link": "7ª DP  Aparecida",
                "ip": "10.11.1.1",
                "regional": True,
                "city_id": 1,
                "phones": [{"number": "48946513"}, {"number": "161651561"}]
            }
        }


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
        if data.phones:
            data.phones = [Phone(**p) for p in data.phones]
        new_object = Workstation(**data.dict())
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


@router.get("/regional", tags=["Workstation"])
async def get_regional(db: Session = Depends(get_db)):
    try:

        all_data = db.query(Workstation).filter(
            Workstation.active == True, Workstation.regional == True).all()
        for d in all_data:
            d.phones = db.query(Phone).filter_by(
                workstation_id=d.id).all()
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


@router.get("/workstation", tags=["Workstation"])
async def get_workstation(
    id: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    try:
        if id:
            workstation = (
                db.query(Workstation)
                .filter(Workstation.id == id, Workstation.active == True)
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
                workstation.phones = db.query(Phone).filter_by(
                    workstation_id=id).all()
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
        for d in all_data:
            d.phones = db.query(Phone).filter_by(
                workstation_id=d.id).all()
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

        workstation: WorkstationModel = db.query(Workstation).filter(
            Workstation.id == workstation_id, Workstation.active == True
        ).one_or_none()

        if not workstation:
            return JSONResponse(
                content={
                    "message": f"Nenhum posto de trabalho com id = {workstation_id} encontrado.",  # noqa E501
                    "error": True,
                    "data": None
                },
                status_code=status.HTTP_200_OK,
            )
        db.query(Phone).filter_by(workstation_id=workstation_id).delete()
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
    "/workstation/{id}",
    tags=["Workstation"]
)
async def put_workstation(data: WorkstationModel,
                          db: Session = Depends(get_db),
                          id: int = Path(title="Workstation id")):
    if data.city_id:
        if not db.query(City).filter(City.id == data.city_id).one_or_none():
            return JSONResponse(
            content={
                "message": f"A cidade de id = {data.city_id} não está cadastrada.",  # noqa E501
                "error": True,
                "data": None,
            }, status_code=status.HTTP_200_OK)
    phones = []
    if data.phones is not None and len(data.phones) > 0:
        db.query(Phone).filter(Phone.workstation_id == id).delete()
        for p in data.phones:
            p['workstation_id'] = id
            db.add(Phone(**p))
            phones.append(Phone(**p))
        db.commit()
    data.phones = None

    if not data.regional and not data.regional_id:
        return JSONResponse(
            content={
                "message": "Caso o posto de trabalho não seja regional, forneça o a regional à qual ele pertence.",
                "error": True,
                "data": None,
            },
            status_code=status.HTTP_200_OK,
        )
    if not db.query(City).filter_by(id=data.city_id).one_or_none():
        return JSONResponse(
            content={
                "message": f"A cidade de id {data.city_id} não está cadastrada.",  # noqa E501
                "error": True,
                "data": None,
            },
            status_code=status.HTTP_200_OK,
        )
    try:
        workstation = db.query(Workstation).filter(
            Workstation.id == id, Workstation.active == True).update(data.dict(exclude_none=True))
        if workstation:
            db.commit()
            workstation = jsonable_encoder(
                db.query(Workstation).filter(Workstation.id == id).first())
            workstation['phones'] = jsonable_encoder(phones)

            return JSONResponse(
                content={
                    "message": "Dados alterados com sucesso",  # noqa E501
                    "error": False,
                    "data": workstation,
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={
                    "message": f"O Posto de Trabalho de id = {id} não está cadastrado.",  # noqa E501
                    "error": True,
                    "data": workstation,
                },
                status_code=status.HTTP_200_OK,
            )

    except Exception as e:
        return JSONResponse(
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
