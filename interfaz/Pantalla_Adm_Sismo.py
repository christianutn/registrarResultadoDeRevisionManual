from modelo.Estado import Estado
from modelo.Estado import inicializar_estados_mock
from modelo.Alcance_Sismo import AlcanceSismo
from modelo.Origen_De_Generacion import OrigenDeGeneracion
from modelo.Estacion_Sismologica import EstacionSismologica
from modelo.Serie_Temporal import SerieTemporal
from modelo.Cambio_Estado import CambioEstado
from modelo.Evento_Sismico import EventoSismico
from datetime import datetime
from controlador.Gestor_Sismo import GestorSismo
import PySimpleGUI as sg
from modelo.Usuario import Usuario
from modelo.Empleado import Empleado

# Create a specific employee
empleado_prueba = Empleado(
    apellido="Perez",
    mail="perez@example.com",
    nombre="Juan",
    telefono="123456789",
    rol="Analista"
)

# Create a specific user and associate it with the employee
usuario_prueba = Usuario(nombre="jperez", contraseña="1234")
usuario_prueba.set_empleado(empleado_prueba)

class PantallaAdmSismo:
    def __init__(self, gestor_sismo):
        self.gestor_sismo = gestor_sismo
        self.usuario_prueba = usuario_prueba
        self.empleado_prueba = empleado_prueba

    def mostrar_menu_opciones(self):
        layout = [
            [sg.Text("Seleccione una opción:")],
            [sg.Button("Registrar resultado de revisión manual"), sg.Button("Salir")]
        ]
        window = sg.Window("Menú Principal", layout)
        opcion = None
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "Salir":
                opcion = "Salir"
                break
            if event == "Registrar resultado de revisión manual":
                opcion = "Registrar resultado de revisión manual"
                break
        window.close()
        return opcion

    def habilitarVentana(self):        # Llama al método registrarResRevManual del gestor
        datos_eventos_ordenados = self.gestor_sismo.registrarResRevManual()
        self.solicitar_elecc_evento_sismico(datos_eventos_ordenados)

    def bloquear_evento(self, evento):
        self.gestor_sismo.bloquear_evento(evento)

    def rechazar_evento(self, evento):
        self.gestor_sismo.rechazar_evento(evento)

    def solicitar_elecc_evento_sismico(self, datos_eventos_ordenados):
        if not datos_eventos_ordenados:
            sg.popup("No hay eventos pendientes de revisión en este momento.")
            return None, None
        layout = [
            [sg.Text("Seleccione un evento sísmico para revisar:")],
            [sg.Listbox(values=[f"{datos['fecha_hora_ocurrencia']} | Epicentro: ({datos['latitud_epicentro']}, {datos['longitud_epicentro']}) | Hipocentro: ({datos['latitud_hipocentro']}, {datos['longitud_hipocentro']}) | Valor magnitud: ({datos['valor_magnitud']})" for datos in datos_eventos_ordenados], size=(80, 10), key="-LISTA-", enable_events=True)],
            [sg.Button("Bloquear"), sg.Button("Salir")]
        ]
        window = sg.Window("Seleccionar Evento Sísmico", layout)
        evento_seleccionado = None
        accion = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Salir":
                accion = "Salir"
                break
            if event in ("Bloquear") and values["-LISTA-"]:
                idx = [f"{datos['fecha_hora_ocurrencia']} | Epicentro: ({datos['latitud_epicentro']}, {datos['longitud_epicentro']}) | Hipocentro: ({datos['latitud_hipocentro']}, {datos['longitud_hipocentro']}) | Valor magnitud: ({datos['valor_magnitud']})" for datos in datos_eventos_ordenados].index(values["-LISTA-"][0])
                evento_seleccionado = datos_eventos_ordenados[idx]
                accion = event
                break
        window.close()
        self.tomar_elecc_evento_sismico(evento_seleccionado, accion)      
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        self.gestor_sismo.tomar_elecc_evento_sismico(evento_seleccionado, accion)
        


if __name__ == "__main__":
    print("--- Inicializando estados mock ---")
    estados_disponibles = inicializar_estados_mock()
    print(f"Estados disponibles: {[e.nombre_estado for e in estados_disponibles]}\n")

    alcance_mock = AlcanceSismo("Regional", "Lejos")
    origen_mock = OrigenDeGeneracion("Argentina", "Automático")
    estacion_mock = EstacionSismologica(
        codigo_estacion="EC001",
        documento_certificacion_adq="cert_doc.pdf",
        fecha_solicitud_certificacion=datetime(2023, 1, 1, 12, 0, 0),
        latitud=-33.5,
        longitud=-70.0,
        nombre="Estacion Central",
        nro_certificacion_adquisicion="CERT1234"
    )

    gestor = GestorSismo()
    pantalla = PantallaAdmSismo(gestor)

    evento1 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 10, 26, 10, 30, 0),
        latitud_epicentro=-33.0,
        longitud_epicentro=-71.0,
        latitud_hipocentro=-33.1,
        longitud_hipocentro=-71.1,
        valor_magnitud=5.5
    )
    evento1.crear_cambio_estado("auto_detectado", "evento_sismico")
    gestor.agregarEvento(evento1)

    evento2 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 11, 15, 14, 0, 0),
        latitud_epicentro=-34.5,
        longitud_epicentro=-70.5,
        latitud_hipocentro=-34.6,
        longitud_hipocentro=-70.6,
        valor_magnitud=4.8
    )
    evento2.crear_cambio_estado("pendiente_revision", "evento_sismico")
    gestor.agregarEvento(evento2)

    evento3 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 12, 1, 9, 0, 0),
        latitud_epicentro=-32.0,
        longitud_epicentro=-72.0,
        latitud_hipocentro=-32.1,
        longitud_hipocentro=-72.1,
        valor_magnitud=6.1
    )
    evento3.crear_cambio_estado("bloqueado", "evento_sismico")
    gestor.agregarEvento(evento3)
    
    evento4 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 12, 5, 15, 0, 0),
        latitud_epicentro=-31.0,
        longitud_epicentro=-71.5,
        latitud_hipocentro=-31.1,
        longitud_hipocentro=-71.6,
        valor_magnitud=4.2
    )
    evento4.crear_cambio_estado("pendiente_revision", "evento_sismico")
    gestor.agregarEvento(evento4)

    evento5 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 11, 20, 18, 30, 0),
        latitud_epicentro=-30.5,
        longitud_epicentro=-70.8,
        latitud_hipocentro=-30.6,
        longitud_hipocentro=-70.9,
        valor_magnitud=5.7
    )
    evento5.crear_cambio_estado("auto_detectado", "evento_sismico")
    gestor.agregarEvento(evento5)

    evento6 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 10, 30, 8, 45, 0),
        latitud_epicentro=-32.5,
        longitud_epicentro=-72.5,
        latitud_hipocentro=-32.6,
        longitud_hipocentro=-72.6,
        valor_magnitud=6.3
    )
    evento6.crear_cambio_estado("rechazado", "evento_sismico")
    gestor.agregarEvento(evento6)

    evento7 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 12, 10, 22, 15, 0),
        latitud_epicentro=-33.2,
        longitud_epicentro=-71.2,
        latitud_hipocentro=-33.3,
        longitud_hipocentro=-71.3,
        valor_magnitud=3.9
    )
    evento7.crear_cambio_estado("pendiente_revision", "evento_sismico")
    gestor.agregarEvento(evento7)

    serie_valores = [0.1, 0.2, 0.3, 0.2, 0.1]
    serie_temporal1 = SerieTemporal(
        condicion_alarma=None,
        fecha_hora_inicio_registro_muestras=datetime(2023, 10, 26, 10, 29, 0),
        fecha_hora_registro=datetime(2023, 10, 26, 10, 29, 0),
        frecuencia_muestreo=100.0
    
    )
    evento1.agregar_serie_temporal(serie_temporal1)
    print(f"Número de series temporales en Evento 1: {len(evento1.obtener_series_temporales())}\n")

    # Mostrar menú principal antes de habilitar ventana
    opcion = pantalla.mostrar_menu_opciones()
    if opcion == "Registrar resultado de revisión manual":
        pantalla.habilitarVentana()
    else:
        print("Saliendo del sistema.")
        exit()

