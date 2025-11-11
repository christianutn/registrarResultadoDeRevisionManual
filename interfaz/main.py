import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMessageBox
from controlador.Gestor_Sismo import GestorSismo
from interfaz.Pantalla_Adm_Sismo import PantallaAdmSismo
from interfaz.menu_opciones import mostrar_menu_opciones
from modelo.Sesion import Sesion
from modelo.Usuario import Usuario
from modelo.Empleado import Empleado
from datetime import datetime

# Importar configuración de base de datos
from config.db import get_session
from models.evento_sismico_model import EventoSismico as EventoSismicoModel
from utils.mappers import evento_model_to_entity

# TODO: Reemplazar datos mock por login real
# Ejemplo de sesión de prueba
empleado_prueba = Empleado(
    apellido="Perez",
    mail="perez@example.com",
    nombre="Juan",
    telefono="123456789",
    rol="Analista"
)

usuario_prueba = Usuario(nombre="jperez", contraseña="1234", empleado=empleado_prueba)
usuario_prueba.set_empleado(empleado_prueba)

sesion_prueba = Sesion(fecha_hora_inicio=datetime.now(), fecha_hora_fin=None, usuario=usuario_prueba)

if __name__ == "__main__":
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    print("🔄 Cargando eventos desde MySQL...")
    
    try:
        # Cargar eventos desde base de datos MySQL
        db_session = get_session()
        eventos_db = db_session.query(EventoSismicoModel).all()
        
        print(f"✅ Encontrados {len(eventos_db)} eventos en la base de datos")
        
        # Convertir modelos a entidades del dominio
        eventos_cargados = []
        for evento_model in eventos_db:
            try:
                evento_entidad = evento_model_to_entity(evento_model)
                eventos_cargados.append(evento_entidad)
            except Exception as e:
                print(f"⚠️ Error convirtiendo evento {evento_model.id}: {e}")
        
        db_session.close()
        
        print(f"✅ Convertidos {len(eventos_cargados)} eventos correctamente")
        
        # Crear gestor y cargar eventos
        gestor = GestorSismo(sesion_prueba)
        for evento in eventos_cargados:
            gestor.agregarEvento(evento)
        
        print(f"✅ Eventos cargados en el gestor: {len(gestor.eventos_sismicos)}")
        
        # Mostrar menú y ejecutar opción
        opcion = mostrar_menu_opciones()
        if opcion == "Registrar resultado de revisión manual":
            pantalla = PantallaAdmSismo(gestor)
            pantalla.opc_res_rev_manual()
        else:
            print("Saliendo del sistema.")
    
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        QMessageBox.critical(
            None,
            "Error de Conexión",
            f"No se pudo conectar a la base de datos:\n{str(e)}\n\nVerifica:\n- MySQL está corriendo\n- Credenciales en config/db.py\n- Base de datos existe"
        )
        sys.exit(1)
    
    sys.exit(0)
