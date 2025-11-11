from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config.db import Base

class EventoSismico(Base):
    __tablename__ = 'evento_sismico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_ocurrencia = Column(DateTime, nullable=True)
    latitud_epicentro = Column(Float, nullable=True)
    latitud_hipocentro = Column(Float, nullable=True)
    longitud_epicentro = Column(Float, nullable=True)
    longitud_hipocentro = Column(Float, nullable=True)
    valor_magnitud = Column(Float, nullable=True)

    alcance_sismo_id = Column(Integer, ForeignKey('alcance_sismo.id'), nullable=False)
    origen_generacion_id = Column(Integer, ForeignKey('origen_de_generacion.id'), nullable=False)
    clasificacion_sismo_id = Column(Integer, ForeignKey('clasificacion_sismo.id'), nullable=False)

    def __repr__(self):
        return (f"<EventoSismico(id={self.id}, magnitud={self.valor_magnitud}, "
                f"fecha={self.fecha_hora_ocurrencia}, "
                f"epicentro=({self.latitud_epicentro}, {self.longitud_epicentro}))>")
