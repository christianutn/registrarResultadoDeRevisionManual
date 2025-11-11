# Migración a Base de Datos MySQL

## ✅ Cambios Realizados

### 1. Limpieza de Código CSV
- ❌ **Eliminado**: Función `cargar_eventos_desde_csv()` de `interfaz/main.py`
- ❌ **Eliminado**: Imports relacionados con CSV (`csv`, `random`, y generación de datos mock)
- ✅ **Mantenido**: Toda la funcionalidad existente del gestor y controladores

### 2. Estructura Preparada para MySQL

#### Archivos Actualizados:
- **`requirements.txt`**: Ahora incluye:
  - `PySide6>=6.6.0` - Interfaz gráfica
  - `SQLAlchemy>=2.0.0` - ORM para MySQL
  - `pymysql>=1.1.0` - Driver de MySQL
  - `cryptography>=41.0.0` - Para conexiones seguras

#### Archivos con TODOs:
- **`interfaz/main.py`**: Contiene ejemplos comentados de cómo cargar datos desde MySQL
- **`controlador/Gestor_Sismo.py`**: TODOs en métodos que consultarán la BD

#### Nuevos Archivos Creados:
- **`utils/mappers.py`**: Conversores entre modelos SQLAlchemy y entidades del dominio
- **`utils/__init__.py`**: Inicializador del paquete utils

### 3. Carpeta `models/` Existente
Ya tienes los modelos SQLAlchemy definidos en:
```
models/
├── __init__.py
├── alcance_sismo_model.py
├── cambio_estado_model.py
├── clasificacion_sismo_model.py
├── detalle_muestra_sismica_model.py
├── empleado_model.py
├── estacion_sismologica_model.py
├── estado_model.py
├── evento_sismico_model.py
├── muestra_sismica_model.py
├── origen_de_generacion_model.py
├── serie_temporal_model.py
├── sesion_model.py
├── sismografo_model.py
├── tipo_de_dato_model.py
└── usuario_model.py
```

### 4. Configuración de Base de Datos
Ya tienes la configuración en:
```
config/
├── db.py                  # Configuración de conexión a MySQL
└── test_connection.py     # Script para probar conexión
```

## 🚀 Pasos para Completar la Migración

### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar Conexión MySQL
Edita `config/db.py` con tus credenciales:
```python
DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost:3306/nombre_bd"
```

### Paso 3: Crear Base de Datos y Tablas
```bash
# Opción A: Si tienes un script de migración
python scripts/init_db.py

# Opción B: Crear manualmente desde los modelos
python -c "from config.db import Base, engine; Base.metadata.create_all(engine)"
```

### Paso 4: Migrar Datos CSV a MySQL (Opcional)
Si quieres migrar los datos del CSV a la BD:

```python
# Crear archivo: scripts/migrate_csv_to_db.py
import csv
from datetime import datetime
from config.db import get_session
from models.evento_sismico_model import EventoSismicoModel
from models.estado_model import EstadoModel

def migrate_csv_to_mysql():
    session = get_session()
    
    with open('eventos_sismicos.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            evento = EventoSismicoModel(
                fecha_hora_ocurrencia=datetime.strptime(
                    row['fecha_hora_ocurrencia'], 
                    '%Y-%m-%d %H:%M:%S'
                ),
                latitud_epicentro=float(row['latitud_epicentro']),
                longitud_epicentro=float(row['longitud_epicentro']),
                latitud_hipocentro=float(row['latitud_hipocentro']),
                longitud_hipocentro=float(row['longitud_hipocentro']),
                valor_magnitud=float(row['valor_magnitud']),
                # ... resto de campos
            )
            session.add(evento)
        
        session.commit()
    print("Migración completada!")

if __name__ == "__main__":
    migrate_csv_to_mysql()
```

Ejecutar:
```bash
python scripts/migrate_csv_to_db.py
```

### Paso 5: Actualizar `interfaz/main.py`
Descomentar y adaptar las líneas marcadas con TODO:

```python
# EN main.py, reemplazar:
# TODO: Cargar eventos desde base de datos MySQL

# POR:
from config.db import get_session
from models.evento_sismico_model import EventoSismicoModel
from utils.mappers import evento_model_to_entity

db_session = get_session()
eventos_db = db_session.query(EventoSismicoModel).filter(
    EventoSismicoModel.estado_actual.in_(['pendiente_revision', 'auto_detectado'])
).all()

eventos_cargados = [evento_model_to_entity(e) for e in eventos_db]

gestor = GestorSismo(sesion_prueba)
for evento in eventos_cargados:
    gestor.agregarEvento(evento)
```

### Paso 6: Actualizar `controlador/Gestor_Sismo.py` (Opcional)
Si quieres que el gestor consulte directamente la BD en lugar de cargar todo en memoria:

```python
def buscar_eventos_para_revisar(self):
    from config.db import get_session
    from models.evento_sismico_model import EventoSismicoModel
    from utils.mappers import evento_model_to_entity
    
    db_session = get_session()
    eventos_db = db_session.query(EventoSismicoModel).filter(
        EventoSismicoModel.estado_actual.in_(['pendiente_revision', 'auto_detectado'])
    ).all()
    
    return [evento_model_to_entity(e) for e in eventos_db]
```

### Paso 7: Probar la Aplicación
```bash
# Probar conexión
python config/test_connection.py

# Ejecutar aplicación
python interfaz/main.py
```

## 📋 Checklist de Migración

- [ ] MySQL instalado y corriendo
- [ ] Credenciales configuradas en `config/db.py`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos creada
- [ ] Tablas creadas (usando SQLAlchemy)
- [ ] Datos migrados desde CSV (opcional)
- [ ] `interfaz/main.py` actualizado con carga desde BD
- [ ] Aplicación probada y funcionando

## 🔍 Verificación

### Probar Conexión a MySQL:
```bash
python config/test_connection.py
```

### Verificar Tablas Creadas:
```python
from config.db import get_session, Base, engine

# Ver todas las tablas
print(Base.metadata.tables.keys())

# Contar eventos en la BD
session = get_session()
from models.evento_sismico_model import EventoSismicoModel
count = session.query(EventoSismicoModel).count()
print(f"Total eventos en BD: {count}")
```

## 🎯 Beneficios de la Migración

1. ✅ **Persistencia Real**: Los cambios de estado se guardan permanentemente
2. ✅ **Escalabilidad**: Soporta grandes volúmenes de datos
3. ✅ **Consultas Eficientes**: SQLAlchemy optimiza las queries
4. ✅ **Integridad**: Relaciones y constraints en la BD
5. ✅ **Concurrencia**: Múltiples usuarios pueden trabajar simultáneamente
6. ✅ **Auditoría**: Historial completo de cambios de estado

## 📚 Recursos

- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)

## ⚠️ Notas Importantes

- Los **estados** siguen usando mock (`inicializar_estados_mock()`) porque son datos de catálogo que no cambian frecuentemente
- Los **mappers** en `utils/mappers.py` convierten entre modelos SQLAlchemy y entidades del dominio
- La **lógica de negocio** NO ha cambiado, solo la capa de persistencia
- Los **archivos Qt** creados anteriormente (`qt_*.py`) están listos para usar con los datos de MySQL

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté corriendo: `sudo systemctl status mysql`
- Verifica host y puerto en `config/db.py`

### Error: "Access denied for user"
- Verifica usuario y contraseña en `config/db.py`
- Otorga permisos: `GRANT ALL PRIVILEGES ON nombre_bd.* TO 'usuario'@'localhost';`

### Error: "No module named 'pymysql'"
- Instala dependencias: `pip install -r requirements.txt`

### Error: "Table doesn't exist"
- Crea las tablas: `python -c "from config.db import Base, engine; Base.metadata.create_all(engine)"`
