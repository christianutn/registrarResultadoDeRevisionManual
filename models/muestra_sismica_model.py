from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class MuestraSismica(Base):
    __tablename__ = 'muestra_sismica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_muestra = Column(DateTime, nullable=False)
    serie_temporal_id = Column(Integer, ForeignKey('serie_temporal.id'), nullable=False)


    def __repr__(self):
        return f"<MuestraSismica(id={self.id}, fecha_hora_muestra={self.fecha_hora_muestra}, serie_temporal_id={self.serie_temporal_id})>"
