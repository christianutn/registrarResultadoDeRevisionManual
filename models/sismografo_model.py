from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Sismografo(Base):
    __tablename__ = 'sismografo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_adquisicion = Column(Date, nullable=True)
    identificador_sismografo = Column(String(45), nullable=True)
    nro_serie = Column(String(45), nullable=True)
    estacion_sismologica_id = Column(Integer, ForeignKey('estacion_sismologica.id'), nullable=False)

    def __repr__(self):
        return (f"<Sismografo(id={self.id}, identificador='{self.identificador_sismografo}', "
                f"nro_serie='{self.nro_serie}', fecha_adquisicion={self.fecha_adquisicion})>")
