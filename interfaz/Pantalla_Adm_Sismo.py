import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import PySimpleGUI as sg
from controlador.Gestor_Sismo import GestorSismo

from modelo.Usuario import Usuario
from modelo.Empleado import Empleado
from modelo.Sesion import Sesion
from datetime import datetime

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
        
    def opc_res_rev_manual(self):
        self.habilitarVentana()

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
            [sg.Button("Bloquear"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Seleccionar Evento Sísmico", layout)
        evento_seleccionado = None
        accion = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                accion = "Cancelar"
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
        self.mostrar_datos_evento_selecc()

    def mostrar_datos_evento_selecc(self):
        datos_series = self.gestor_sismo.buscar_datos_series_temporales()
        print("Datos de series temporales obtenidos exitosamente")
        if isinstance(datos_series, dict):
            texto = ""
            for estacion, series in datos_series.items():
                texto += f"\n{estacion}\n"
                for serie in series:
                    texto += f"  Serie: {serie}\n"
        else:
            texto = str(datos_series)
        # Nueva ventana con botones
        layout = [
            [sg.Multiline(texto, size=(80, 20), disabled=True)],
            [sg.Button("Ver mapa"), sg.Button("Modificar evento"), sg.Button("Siguiente"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Series temporales por estación", layout)
        cerrar_todo = False
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                cerrar_todo = True
                break
            if event == "Siguiente":
                break
            if event == "Ver mapa":
                self.habilitar_opc_mapa()
            if event == "Modificar evento":
                self.habilitar_opc_modificar_evento()
        window.close()
        if cerrar_todo:
            return  # Sale completamente, no muestra la ventana de acción
        # Directamente mostrar la ventana de acción y manejar la selección aquí
        window_accion = self.solicitar_selecc_opc_accion()
        self.tomar_selecc_opc_accion(window_accion)

    def solicitar_selecc_opc_accion(self):
        layout = [
            [sg.Text("Seleccione una acción para el evento sísmico:")],
            [sg.Button("Confirmar evento"), sg.Button("Rechazar evento"), sg.Button("Solicitar revisión a experto"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Acción sobre evento sísmico", layout)
        # Solo muestra la ventana y retorna el objeto window para que la selección se haga en el otro método
        return window

    def tomar_selecc_opc_accion(self, window):    
        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                break
            if event in ("Confirmar evento", "Rechazar evento", "Solicitar revisión a experto"):
                # Validar la acción con el gestor
                valido, mensaje = self.gestor_sismo.tomar_selecc_opc_accion(event)
                if not valido:
                    sg.popup(mensaje)
                    continue
                # Si es válido, cambiar el estado del evento
                self.gestor_sismo.cambiar_estado_evento_sismico(self.gestor_sismo.evento_seleccionado, event)
                if event == "Confirmar evento":
                    sg.popup("Evento confirmado. Estado actualizado y responsable registrado.")
                elif event == "Rechazar evento":
                    sg.popup("Evento rechazado. Estado actualizado y responsable registrado.")
                elif event == "Solicitar revisión a experto":
                    sg.popup("Revisión a experto solicitada. Estado actualizado y responsable registrado.")
                break
        window.close()

    def habilitar_opc_mapa(self):
        sg.popup("Opción de mapa habilitada para el evento seleccionado. Acá se mostraría el mapa con la ubicación del evento y estaciones asociadas")

    def habilitar_opc_modificar_evento(self):
        sg.popup("Opción para modificar los datos del evento sísmico habilitada. Acá se permitiría editar los datos del evento seleccionado.")
