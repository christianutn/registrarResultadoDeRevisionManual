# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔗 Cadena de conexión
# Sintaxis: mysql+pymysql://usuario:contraseña@host:puerto/nombre_base
DATABASE_URL = "mysql+pymysql://root:Cairo2024@localhost/bd_dsi"

# ⚙️ Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)  # echo=True muestra las consultas SQL

# 🧠 Crear la sesión (se usa para interactuar con la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base para definir modelos (tablas)
Base = declarative_base()
