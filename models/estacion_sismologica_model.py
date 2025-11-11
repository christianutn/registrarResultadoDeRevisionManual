# models/estacion_sismologica.model.py
from sqlalchemy import Column, Integer, String, Float, Date
from config.db import Base

class EstacionSismologica(Base):
    __tablename__ = 'estacion_sismologica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_estacion = Column(String(45), nullable=False)
    documento_certificacion_adq = Column(String(45), nullable=False)
    fecha_solicitud_certificacion = Column(Date, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    nombre = Column(String(45), nullable=False)
    nro_certificacion_adquisicion = Column(String(45), nullable=False)

    def __repr__(self):
        return (
            f"<EstacionSismologica("
            f"id={self.id}, "
            f"codigo_estacion='{self.codigo_estacion}', "
            f"documento_certificacion_adq='{self.documento_certificacion_adq}', "
            f"fecha_solicitud_certificacion={self.fecha_solicitud_certificacion}, "
            f"latitud={self.latitud}, "
            f"longitud={self.longitud}, "
            f"nombre='{self.nombre}', "
            f"nro_certificacion_adquisicion='{self.nro_certificacion_adquisicion}'"
            f")>"
        )
