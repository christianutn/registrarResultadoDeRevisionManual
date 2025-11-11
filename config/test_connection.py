import sys
import os

# 🔧 Aseguramos que el proyecto esté en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import SessionLocal, Base, engine
from models import EventoSismico  # 👈 Importas directamente desde el paquete models

# 🔨 (opcional) crea las tablas si aún no existen
Base.metadata.create_all(bind=engine)

# 🧠 Creamos la sesión
db = SessionLocal()

try:
    # Consultar todos los registros
    eventos = db.query(EventoSismico).all()

    if not eventos:
        print("No hay registros en evento_sismico.")
    else:
        for e in eventos:
            print(e)

except Exception as ex:
    print("❌ Error al consultar la base de datos:", ex)

finally:
    db.close()
