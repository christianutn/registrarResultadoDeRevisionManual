import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from modelo.Estado import Estado, inicializar_estados_mock
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
from modelo.Sesion import Sesion
from modelo.Clasificacion_Sismo import ClasificacionSismo
from interfaz.menu_opciones import mostrar_menu_opciones


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

class PantallaAdmSismo:
    def __init__(self, gestor_sismo):
        self.gestor_sismo = gestor_sismo
        self.sesion_prueba = sesion_prueba

    def habilitarVentana(self):
        # Recibe dos valores: la lista de dicts y la lista de objetos
        datos_eventos_ordenados, eventos_objetos = self.gestor_sismo.registrarResRevManual()
        self.solicitar_elecc_evento_sismico(datos_eventos_ordenados, eventos_objetos)


    def solicitar_elecc_evento_sismico(self, datos_eventos_ordenados, eventos_objetos):
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
                evento_seleccionado = eventos_objetos[idx]  
                accion = event
                break
        window.close()
        self.tomar_elecc_evento_sismico(evento_seleccionado, accion)      
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        if evento_seleccionado is None:
            sg.popup("Hasta luego")
            return
        self.gestor_sismo.tomar_elecc_evento_sismico(evento_seleccionado, accion)
        print("Evento bloqueado exitosamente")