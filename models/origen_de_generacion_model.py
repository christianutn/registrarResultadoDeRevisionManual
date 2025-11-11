# models/origen_de_generacion.model.py
from sqlalchemy import Column, Integer, String
from config.db import Base

class OrigenDeGeneracion(Base):
    __tablename__ = 'origen_de_generacion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=True)
    nombre = Column(String(45), nullable=False)

    def __repr__(self):
        return (
            f"<OrigenDeGeneracion("
            f"id={self.id}, "
            f"nombre='{self.nombre}', "
            f"descripcion='{self.descripcion}'"
            f")>"
        )
