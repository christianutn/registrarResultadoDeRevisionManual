import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controlador.Gestor_Sismo import GestorSismo
from interfaz.Pantalla_Adm_Sismo import PantallaAdmSismo
from interfaz.menu_opciones import mostrar_menu_opciones
from modelo.Sesion import Sesion
from modelo.Usuario import Usuario
from modelo.Empleado import Empleado
from modelo.Estado import inicializar_estados_mock
from datetime import datetime
import csv
import random
from modelo.Evento_Sismico import EventoSismico
from modelo.Cambio_Estado import CambioEstado

def cargar_eventos_desde_csv(ruta_csv):
    eventos = []
    estados_disponibles = inicializar_estados_mock()

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            evento = EventoSismico(
                fecha_hora_ocurrencia=datetime.strptime(fila['fecha_hora_ocurrencia'], '%Y-%m-%d %H:%M:%S'),
                latitud_epicentro=float(fila['latitud_epicentro']),
                longitud_epicentro=float(fila['longitud_epicentro']),
                latitud_hipocentro=float(fila['latitud_hipocentro']),
                longitud_hipocentro=float(fila['longitud_hipocentro']),
                valor_magnitud=float(fila['valor_magnitud']),
                cambio_estado=[]  # Los cambios de estado pueden ser cargados aparte si es necesario
            )
            # Validar y asignar clasificaciones, orígenes y alcances
            evento.validar_y_asignar_clasificacion(fila['clasificacion_sismo'])
            evento.validar_y_asignar_origen(fila['origen_de_generacion'])
            evento.validar_y_asignar_alcance(fila['alcance_sismo'])

            # Asignar un estado inicial aleatorio de los disponibles
            estado_inicial = random.choice(estados_disponibles)

            # Registrar el cambio de estado inicial
            if estado_inicial:
                cambio_estado_inicial = CambioEstado(
                    fecha_hora_inicio=datetime.now(),
                    estado=estado_inicial,
                    empleado=None  # No hay empleado asociado al estado inicial
                )
                evento.cambio_estado.append(cambio_estado_inicial)
                evento.estado_actual = cambio_estado_inicial

            eventos.append(evento)
    return eventos

# Create a specific employee
empleado_prueba = Empleado(
    apellido="Perez",
    mail="perez@example.com",
    nombre="Juan",
    telefono="123456789",
    rol="Analista"
)

# Create a specific user and associate it with the employee
usuario_prueba = Usuario(nombre="jperez", contraseña="1234", empleado=empleado_prueba)
usuario_prueba.set_empleado(empleado_prueba)

# Create a session and associate it with the user
sesion_prueba = Sesion(fecha_hora_inicio=datetime.now(), fecha_hora_fin=None, usuario=usuario_prueba)

if __name__ == "__main__":
    # Cargar eventos desde el archivo CSV
    ruta_csv = "c:\\Users\\Martin Ferreyra\\OneDrive\\Desktop\\SISTEMAS\\TERCER AÑO\\DSI\\PRÁCTICO\\PPAI\\registrarResultadoDeRevisionManual\\eventos_sismicos.csv"
    eventos_cargados = cargar_eventos_desde_csv(ruta_csv)

    gestor = GestorSismo(sesion_prueba)

    # Agregar eventos cargados al gestor
    for evento in eventos_cargados:
        gestor.agregarEvento(evento)

    pantalla = PantallaAdmSismo(gestor) # VEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEER

    # Mostrar menú principal antes de habilitar ventana
    opcion = mostrar_menu_opciones()
    if opcion == "Registrar resultado de revisión manual":
        pantalla.opcRegResManual()
    else:
        print("Saliendo del sistema.")
        exit()
