from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    contraseña = Column(String(45), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleado.id"), nullable=True)


    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', empleado_id={self.empleado_id})>"
