# models/clasificacion_sismo.model.py
from sqlalchemy import Column, Integer, Float, String
from config.db import Base

class ClasificacionSismo(Base):
    __tablename__ = 'clasificacion_sismo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    km_profundidad_desde = Column(Float, nullable=True)
    km_profundidad_hasta = Column(Float, nullable=True)
    nombre = Column(String(45), nullable=False)

    def __repr__(self):
        return (
            f"<ClasificacionSismo("
            f"id={self.id}, "
            f"nombre='{self.nombre}', "
            f"km_profundidad_desde={self.km_profundidad_desde}, "
            f"km_profundidad_hasta={self.km_profundidad_hasta}"
            f")>"
        )