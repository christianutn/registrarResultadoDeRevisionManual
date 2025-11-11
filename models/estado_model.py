from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ambito = Column(String(45), nullable=False)
    nombre_estado = Column(String(45), nullable=False)
    es_bloqueado = Column(Boolean, default=False)
    es_rechazado = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<Estado(id={self.id}, ambito='{self.ambito}', "
                f"nombre_estado='{self.nombre_estado}', "
                f"es_bloqueado={self.es_bloqueado}, es_rechazado={self.es_rechazado})>")
