from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)


class Workstation(Base):
    __tablename__ = "workstation"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    adsl_vpn = Column(Boolean, nullable=False)
    link = Column(String(250), nullable=True)
    ip = Column(String(250), nullable=True)
    regional = Column(Boolean, nullable=False, default=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    regional_id = Column(Integer, ForeignKey("workstation.id"), nullable=True)


phone = Table(
    "phone",
    Base.metadata,
    Column("id_workstation", Integer, ForeignKey("workstation.id")),
    Column("phone", String(250), nullable=False),
)

