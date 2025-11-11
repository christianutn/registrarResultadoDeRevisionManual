from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CambioEstado(Base):
    __tablename__ = 'cambio_estado'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_fin = Column(DateTime, nullable=True)
    fecha_hora_inicio = Column(DateTime, nullable=True)
    estado_id = Column(Integer, ForeignKey('estado.id'), nullable=False)
    evento_sismico_id = Column(Integer, ForeignKey('evento_sismico.id'), nullable=False)
    empleado_id = Column(Integer, ForeignKey('empleado.id'), nullable=False)

  

    def __repr__(self):
        return (f"<CambioEstado(id={self.id}, estado_id={self.estado_id}, "
                f"evento_sismico_id={self.evento_sismico_id}, empleado_id={self.empleado_id}, "
                f"fecha_inicio={self.fecha_hora_inicio}, fecha_fin={self.fecha_hora_fin})>")
