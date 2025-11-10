import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import PySimpleGUI as sg
from controlador.Gestor_Sismo import GestorSismo


class PantallaAdmSismo:
    def __init__(self, gestor_sismo):
        self.gestor_sismo = gestor_sismo

    def opc_res_rev_manual(self):
        self.habilitarVentana()

    def habilitarVentana(self):
        datos_eventos_ordenados, eventos_objetos = self.gestor_sismo.registrarResRevManual()
        self.solicitar_elecc_evento_sismico(datos_eventos_ordenados, eventos_objetos)

    def solicitar_elecc_evento_sismico(self, datos_eventos_ordenados, eventos_objetos):
        """Muestra una tabla amigable con los eventos pendientes y permite bloquear uno."""
        if not datos_eventos_ordenados:
            sg.popup("No hay eventos pendientes de revisión en este momento.", title="Sin eventos")
            return None, None

        # Preparar filas para la tabla
        headings = ["Fecha/Hora", "Epicentro (lat,lon)", "Hipocentro (lat,lon)", "Magnitud"]
        table_values = []
        for datos in datos_eventos_ordenados:
            fecha = str(datos.get('fecha_hora_ocurrencia'))
            epic = f"{datos.get('latitud_epicentro')}, {datos.get('longitud_epicentro')}"
            hipo = f"{datos.get('latitud_hipocentro')}, {datos.get('longitud_hipocentro')}"
            mag = str(datos.get('valor_magnitud'))
            table_values.append([fecha, epic, hipo, mag])

        # Aplicar tema de forma compatible con distintas versiones de PySimpleGUI
        if hasattr(sg, 'theme'):
            sg.theme('DarkBlue3')
        elif hasattr(sg, 'ChangeLookAndFeel'):
            try:
                sg.ChangeLookAndFeel('DarkBlue3')
            except Exception:
                pass
        else:
            pass

        layout = [
            [sg.Text("Seleccione un evento sísmico para revisar:", font=("Segoe UI", 12))],
            [
                sg.Table(values=table_values, headings=headings, max_col_width=40,
                         auto_size_columns=False,
                         col_widths=[25, 20, 20, 10],
                         display_row_numbers=True,
                         justification='left',
                         num_rows=10,
                         key='-TABLE-',
                         enable_events=True,
                         select_mode=sg.TABLE_SELECT_MODE_BROWSE),
            ],
            [sg.Button("🔒 Bloquear evento", key='-BLOQUEAR-', button_color=("white", "#2a9d8f")), sg.Button("Cancelar", key='-CANCELAR-')]
        ]

        window = sg.Window("Seleccionar Evento Sísmico", layout, element_justification='center', modal=True)
        evento_seleccionado = None
        accion = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == '-CANCELAR-':
                accion = "Cancelar"
                break
            if event == '-BLOQUEAR-':
                selected = values.get('-TABLE-')
                if not selected:
                    sg.popup("Por favor seleccione un evento de la lista.", title="Atención")
                    continue
                idx = selected[0]
                evento_seleccionado = eventos_objetos[idx]
                accion = 'Bloquear'
                break
        window.close()
        self.tomar_elecc_evento_sismico(evento_seleccionado, accion)

    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        if evento_seleccionado is None:
            return
        self.gestor_sismo.tomar_elecc_evento_sismico(evento_seleccionado, accion)
        sg.popup("Evento bloqueado exitosamente", title="Bloqueo")
        self.mostrar_datos_evento_selecc()

    def mostrar_datos_evento_selecc(self):
        datos_series = self.gestor_sismo.buscar_datos_series_temporales()
        # Formatear el texto de detalle
        if isinstance(datos_series, dict):
            lines = []
            for estacion, series in datos_series.items():
                lines.append(f"== {estacion} ==")
                for serie in series:
                    lines.append(f"  - Serie: {serie}")
            texto = "\n".join(lines)
        else:
            texto = str(datos_series)

        layout = [
            [sg.Multiline(texto, size=(100, 20), disabled=True, font=("Consolas", 10))],
            [
                sg.Button("🗺️ Ver mapa", key='-MAPA-'),
                sg.Button("✏️ Modificar evento", key='-MODIFICAR-'),
                sg.Button("Siguiente", key='-SIG-'),
                sg.Button("Cancelar", key='-CANCEL-')
            ]
        ]
        window = sg.Window("Series temporales por estación", layout, modal=True)
        cerrar_todo = False
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
                cerrar_todo = True
                break
            if event == '-SIG-':
                break
            if event == '-MAPA-':
                self.habilitar_opc_mapa()
            if event == '-MODIFICAR-':
                self.habilitar_opc_modificar_evento()
        window.close()
        if cerrar_todo:
            return
        window_accion = self.solicitar_selecc_opc_accion()
        self.tomar_selecc_opc_accion(window_accion)

    def solicitar_selecc_opc_accion(self):
        layout = [
            [sg.Text("Seleccione una acción para el evento sísmico:", font=("Segoe UI", 11))],
            [
                sg.Button("✅ Confirmar evento", key='-CONF-', button_color=("white", "#2a9d8f")),
                sg.Button("❌ Rechazar evento", key='-RECH-'),
                sg.Button("🔔 Solicitar revisión a experto", key='-EXPR-'),
                sg.Button("Cancelar", key='-CAN-')
            ]
        ]
        window = sg.Window("Acción sobre evento sísmico", layout, modal=True, element_justification='center')
        return window

    def tomar_selecc_opc_accion(self, window):
        while True:
            event, _ = window.read()
            if event in (sg.WINDOW_CLOSED, '-CAN-'):
                break
            if event in ('-CONF-', '-RECH-', '-EXPR-'):
                # Mapear keys a texto que usa el gestor
                mapping = {'-CONF-': 'Confirmar evento', '-RECH-': 'Rechazar evento', '-EXPR-': 'Solicitar revisión a experto'}
                action_text = mapping[event]
                valido, mensaje = self.gestor_sismo.tomar_selecc_opc_accion(action_text)
                if not valido:
                    sg.popup(mensaje, title="Error")
                    continue
                self.gestor_sismo.cambiar_estado_evento_sismico(self.gestor_sismo.evento_seleccionado, action_text)
                if event == '-CONF-':
                    sg.popup("Evento confirmado. Estado actualizado y responsable registrado.")
                elif event == '-RECH-':
                    sg.popup("Evento rechazado. Estado actualizado y responsable registrado.")
                elif event == '-EXPR-':
                    sg.popup("Revisión a experto solicitada. Estado actualizado y responsable registrado.")
                break
        window.close()

    def habilitar_opc_mapa(self):
        sg.popup("Opción de mapa habilitada para el evento seleccionado. Aquí se podría mostrar un mapa interactivo.", title="Mapa")

    def habilitar_opc_modificar_evento(self):
        sg.popup("Opción para modificar los datos del evento sísmico habilitada. Aquí se podría abrir un formulario de edición.", title="Modificar evento")
