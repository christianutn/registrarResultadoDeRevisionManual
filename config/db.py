# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔗 Cadena de conexión
# Sintaxis: mysql+pymysql://usuario:contraseña@host:puerto/nombre_base
DATABASE_URL = "mysql+pymysql://root:root@localhost/bd_dsi"

# ⚙️ Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=False)  # echo=False para no mostrar SQL en consola

# 🧠 Crear la sesión (se usa para interactuar con la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Base para definir modelos (tablas)
Base = declarative_base()


def get_session():
    """
    Obtiene una nueva sesión de base de datos.
    Usar con context manager para cerrar automáticamente:
    
    with get_session() as session:
        eventos = session.query(EventoSismico).all()
    """
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        session.close()
        raise e
