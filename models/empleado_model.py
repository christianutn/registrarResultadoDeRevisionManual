# models/empleado.model.py
from sqlalchemy import Column, Integer, String
from config.db import Base

class Empleado(Base):
    __tablename__ = 'empleado'

    id = Column(Integer, primary_key=True, autoincrement=True)
    apellido = Column(String(45), nullable=False)
    nombre = Column(String(45), nullable=False)
    telefono = Column(String(10), nullable=True)
    mail = Column(String(100), nullable=True)

    def __repr__(self):
        return (
            f"<Empleado("
            f"id={self.id}, "
            f"apellido='{self.apellido}', "
            f"nombre='{self.nombre}', "
            f"telefono='{self.telefono}', "
            f"mail='{self.mail}'"
            f")>"
        )
