from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)


class Workstation(Base):
    __tablename__ = "workstation"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    asdl_vpn = Column(Boolean, nullable=False)
    link = Column(String(250), nullable=True)
    ip = Column(String(250), nullable=True)
    regional = Column(Boolean, nullable=False, default=False)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    regional_id = Column(Integer, ForeignKey("workstation.id"), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    phones = relationship("Phone", backref=backref(
        "workstation", cascade="all"))


class Phone(Base):
    __tablename__ = "phone"
    id = Column(Integer, primary_key=True)
    workstation_id = Column("workstation_id", Integer,
                            ForeignKey("workstation.id"))
    number = Column("number", String(250), nullable=False)
    # workstation = relationship("Workstation", , back_populates="phones")
