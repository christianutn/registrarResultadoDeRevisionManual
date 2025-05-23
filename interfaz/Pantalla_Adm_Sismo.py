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

class PantallaAdmSismo:
    def __init__(self, gestor_sismo):
        self.gestor_sismo = gestor_sismo

    def mostrar_eventos_para_revisar(self):
        eventos = self.gestor_sismo.buscar_eventos_para_revisar()
        if not eventos:
            sg.popup("No hay eventos pendientes de revisión en este momento.")
            return []
        layout = [
            [sg.Text("Eventos Sísmicos Pendientes de Revisión")],
            [sg.Listbox(values=[f"{i+1}. {e.obtener_datos_evento()['fecha_hora_ocurrencia']} | Epicentro: ({e.obtener_datos_evento()['latitud_epicentro']}, {e.obtener_datos_evento()['longitud_epicentro']}) | Estado: {e.obtener_datos_evento()['estado_actual']}" for i, e in enumerate(eventos)], size=(80, 10), key="-LISTA-", enable_events=True)],
            [sg.Button("Bloquear"), sg.Button("Rechazar"), sg.Button("Salir")]
        ]
        window = sg.Window("Eventos para Revisar", layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Salir":
                break
            if event == "Bloquear" and values["-LISTA-"]:
                idx = [f"{i+1}." for i in range(len(eventos))].index(values["-LISTA-"][0].split()[0])
                self.bloquear_evento(eventos[idx])
                sg.popup("Evento bloqueado")
            if event == "Rechazar" and values["-LISTA-"]:
                idx = [f"{i+1}." for i in range(len(eventos))].index(values["-LISTA-"][0].split()[0])
                self.rechazar_evento(eventos[idx])
                sg.popup("Evento rechazado")
        window.close()
        return eventos

    def bloquear_evento(self, evento):
        self.gestor_sismo.bloquear_evento(evento)

    def rechazar_evento(self, evento):
        self.gestor_sismo.rechazar_evento(evento)


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
    evento1.crear_cambio_estado("Auto detectado")
    gestor.agregarEvento(evento1)

    evento2 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 11, 15, 14, 0, 0),
        latitud_epicentro=-34.5,
        longitud_epicentro=-70.5,
        latitud_hipocentro=-34.6,
        longitud_hipocentro=-70.6,
        valor_magnitud=4.8
    )
    evento2.crear_cambio_estado("Pendiente revision")
    gestor.agregarEvento(evento2)

    evento3 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2023, 12, 1, 9, 0, 0),
        latitud_epicentro=-32.0,
        longitud_epicentro=-72.0,
        latitud_hipocentro=-32.1,
        longitud_hipocentro=-72.1,
        valor_magnitud=6.1
    )
    evento3.crear_cambio_estado("Bloqueado")
    gestor.agregarEvento(evento3)

    serie_valores = [0.1, 0.2, 0.3, 0.2, 0.1]
    serie_temporal1 = SerieTemporal(
        condicion_alarma=None,
        fecha_hora_inicio_registro_muestras=datetime(2023, 10, 26, 10, 29, 0),
        fecha_hora_registro=datetime(2023, 10, 26, 10, 29, 0),
        frecuencia_muestreo=100.0
    )
    evento1.agregar_serie_temporal(serie_temporal1)
    print(f"Número de series temporales en Evento 1: {len(evento1.obtener_series_temporales())}\n")

    eventos_a_revisar = pantalla.mostrar_eventos_para_revisar()

    (evento2)
    if eventos_a_revisar:
        print("\n--- Simulación de bloqueo de evento ---")
        pantalla.opcion_bloquear_evento(eventos_a_revisar[0]) 
        print(f"Estado del Evento 2 después de la acción: {evento2.get_estado_actual().estado.nombre_estado}")

    
    print("\n--- Eventos pendientes de revisión después del bloqueo ---")
    pantalla.mostrar_eventos_para_revisar()

 
    print("\n--- Escenario 2: Rechazar un evento ---")
    evento4 = EventoSismico(
        fecha_hora_ocurrencia=datetime(2024, 1, 10, 8, 0, 0),
        latitud_epicentro=-35.0,
        longitud_epicentro=-71.0,
        latitud_hipocentro=-35.1,
        longitud_hipocentro=-71.1,
        valor_magnitud=5.9
    )
    evento4.crear_cambio_estado("Pendiente revision")
    gestor.agregarEvento(evento4)


    eventos_a_revisar_2 = pantalla.mostrar_eventos_para_revisar()
    if eventos_a_revisar_2:
        print("\n--- Simulación de rechazo de evento ---")
        pantalla.opcion_rechazar_evento(eventos_a_revisar_2[0]) 
        print(f"Estado del Evento 4 después de la acción: {evento4.get_estado_actual().estado.nombre_estado}")




    print("\n--- Eventos pendientes de revisión después del rechazo ---")
    pantalla.mostrar_eventos_para_revisar()