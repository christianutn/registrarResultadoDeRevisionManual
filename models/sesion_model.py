from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Sesion(Base):
    __tablename__ = 'sesion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)


    def __repr__(self):
        return (f"<Sesion(id={self.id}, usuario_id={self.usuario_id}, "
                f"inicio={self.fecha_hora_inicio}, fin={self.fecha_hora_fin})>")
