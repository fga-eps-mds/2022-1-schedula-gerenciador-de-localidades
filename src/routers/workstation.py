from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from database import engine, get_db
from models import Base, City, Workstation

router = APIRouter()


class WorkstationModel(BaseModel):
    name: str
    asdl_vpn: bool
    link: str | None = None
    ip: str | None = None
    regional: bool = False
    city_id: int
    regional_id: int | None = None
    active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "2ª DRP - Aparecida",
                "asdl_vpn": True,
                "link": "7ª DP  Aparecida",
                "ip": "10.11.1.1",
                "regional": True,
                "city_id": 1
            }
        }

    Base.metadata.create_all(bind=engine)


@router.delete("/workstation/{workstation_id}", tags=["Workstation"], response_model=WorkstationModel)
async def delete_workstation(workstation_id: int, db: Session = Depends(get_db)):
    try:
        workstation: WorkstationModel = db.query(
            Workstation).filter_by(id=workstation_id).one_or_none()
        if not workstation:
            return JSONResponse(
                content={
                    "message": f"Nenhum posto de trabalho com id = {workstation_id} encontrado.",
                    "error": True,
                    "data": None,
                }, status_code=status.HTTP_400_BAD_REQUEST
            )
        workstation.active = False
        db.add(workstation)
        db.commit()
        return JSONResponse(
            content={
                "message": f"Posto de trabalho de id = {workstation_id} deletado com sucesso",
                "error": True,
                "data": None,
            }, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(
            content={
                "message": "Erro ao processar dados",
                "error": str(e),
                "data": None,
            }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
