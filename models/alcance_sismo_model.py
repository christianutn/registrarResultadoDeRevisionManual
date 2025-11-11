from sqlalchemy import Column, Integer, String
from config.db import Base

class AlcanceSismo(Base):
    __tablename__ = "alcance_sismo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=True)
    nombre = Column(String(45), nullable=False)

    def __repr__(self):
        return f"<AlcanceSismo(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}')>"
