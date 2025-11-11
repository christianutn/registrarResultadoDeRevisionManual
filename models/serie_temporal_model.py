from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class SerieTemporal(Base):
    __tablename__ = 'serie_temporal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    condicion_alarma = Column(String(45), nullable=True)
    fecha_hora_registro_muestras = Column(DateTime, nullable=True)
    fecha_hora_registro = Column(DateTime, nullable=True)
    frecuencia_muestreo = Column(Float, nullable=True)

    sismografo_id = Column(Integer, ForeignKey('sismografo.id'), nullable=True)
    evento_sismico_id = Column(Integer, ForeignKey('evento_sismico.id'), nullable=True)

    def __repr__(self):
        return (f"<SerieTemporal(id={self.id}, alarma={self.condicion_alarma}, "
                f"registro={self.fecha_hora_registro}, frecuencia={self.frecuencia_muestreo})>")
