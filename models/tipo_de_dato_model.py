# models/tipo_de_dato.model.py
from sqlalchemy import Column, Integer, String, Float
from config.db import Base

class TipoDeDato(Base):
    __tablename__ = 'tipo_de_dato'

    id = Column(Integer, primary_key=True, autoincrement=True)
    denominacion = Column(String(45), nullable=True)
    nombre_unidad_medida = Column(String(45), nullable=True)
    valor_umbral = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<TipoDeDato("
            f"id={self.id}, "
            f"denominacion='{self.denominacion}', "
            f"nombre_unidad_medida='{self.nombre_unidad_medida}', "
            f"valor_umbral={self.valor_umbral}"
            f")>"
        )
