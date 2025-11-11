from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class DetalleMuestraSismica(Base):
    __tablename__ = 'detalle_muestra_sismica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)

    tipo_de_dato_id = Column(Integer, ForeignKey('tipo_de_dato.id'), nullable=False)
    muestra_sismica_id = Column(Integer, ForeignKey('muestra_sismica.id'), nullable=False)


    def __repr__(self):
        return (f"<DetalleMuestraSismica(id={self.id}, valor={self.valor}, "
                f"tipo_de_dato_id={self.tipo_de_dato_id}, "
                f"muestra_sismica_id={self.muestra_sismica_id})>")
