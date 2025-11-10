import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Use PySimpleGUIQt for a nicer Qt-based appearance; API stays compatible
from interfaz.sg_backend import sg
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
        if not datos_eventos_ordenados:
            sg.popup("No hay eventos pendientes de revisión en este momento.")
            return None, None
        # preparo la lista con más información: alcance, origen y clasificación
        lista_valores = []
        for datos in datos_eventos_ordenados:
            fecha = datos.get('fecha_hora_ocurrencia')
            epic = f"({datos.get('latitud_epicentro')}, {datos.get('longitud_epicentro')})"
            hip = f"({datos.get('latitud_hipocentro')}, {datos.get('longitud_hipocentro')})"
            mag = datos.get('valor_magnitud')
            alcance = datos.get('alcance_sismo') if datos.get('alcance_sismo') is not None else 'N/D'
            origen = datos.get('origen_generacion') if datos.get('origen_generacion') is not None else 'N/D'
            clasif = datos.get('clasificacion_sismo') if datos.get('clasificacion_sismo') is not None else 'N/D'
            lista_valores.append(f"{fecha} | Epicentro: {epic} | Hipocentro: {hip} | Magnitud: {mag} | Alcance: {alcance} | Origen: {origen} | Clasif.: {clasif}")

        layout = [
            [sg.Text("Seleccione un evento sísmico para revisar:")],
            [sg.Listbox(values=lista_valores, size=(120, 10), key="-LISTA-", enable_events=True)],
            # Se eliminó el botón "Bloquear": el bloqueo lo realiza el sistema según el CU
            [sg.Button("Seleccionar"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Seleccionar Evento Sísmico", layout)
        evento_seleccionado = None
        accion = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                accion = "Cancelar"
                break
            if event == "Seleccionar" and values["-LISTA-"]:
                try:
                    idx = lista_valores.index(values["-LISTA-"][0])
                except ValueError:
                    idx = 0
                evento_seleccionado = eventos_objetos[idx]
                accion = "Seleccionar"
                break
        window.close()
        self.tomar_elecc_evento_sismico(evento_seleccionado, accion)
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        if evento_seleccionado is None:
            return
        # La selección sólo elige el evento; no debe cambiar su estado inmediatamente.
        if accion == "Seleccionar":
            # conservar la referencia al evento seleccionado en el gestor pero no cambiar su estado
            self.gestor_sismo.evento_seleccionado = evento_seleccionado
            print(f"Evento seleccionado: {evento_seleccionado}")
        else:
            # otras acciones sí disparan cambios de estado
            self.gestor_sismo.tomar_elecc_evento_sismico(evento_seleccionado, accion)
            print(f"Acción tomada: {accion}")
        self.mostrar_datos_evento_selecc()

    def mostrar_datos_evento_selecc(self):
        datos_series = self.gestor_sismo.buscar_datos_series_temporales()
        print("Datos de series temporales obtenidos exitosamente")
        texto = ""
        if isinstance(datos_series, dict):
            for estacion, series in datos_series.items():
                texto += f"\nEstación: {estacion}\n"
                for serie in series:
                    # espero estructura [muestras, codigo, nombre]
                    try:
                        muestras = serie[0]
                        codigo = serie[1]
                        nombre = serie[2]
                    except Exception:
                        texto += f"  Serie: {serie}\n"
                        continue
                    texto += f"  Código: {codigo} | Nombre: {nombre}\n"
                    texto += f"    Cantidad de muestras: {len(muestras) if hasattr(muestras, '__len__') else 'N/D'}\n"
                    # muestro hasta 2 ejemplos de muestras por serie
                    if hasattr(muestras, '__iter__'):
                        for i, muestra in enumerate(list(muestras)[:2]):
                            texto += f"      Ejemplo muestra {i+1}: {muestra}\n"
        else:
            texto = str(datos_series)

        # Mostrar las 5 opciones según el CU: Ver mapa, Modificar evento, y las 3 acciones finales
        layout = [
            [sg.Multiline(texto, size=(100, 20), disabled=True)],
            [
                sg.Button("Ver mapa"), sg.Button("Modificar evento"),
                sg.Button("Confirmar evento"), sg.Button("Rechazar evento"), sg.Button("Solicitar revisión a experto"),
                sg.Button("Cancelar")
            ]
        ]
        window = sg.Window("Series temporales por estación", layout)
        accion_seleccionada = None
        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                window.close()
                return
            if event == "Ver mapa":
                self.habilitar_opc_mapa()
                continue
            if event == "Modificar evento":
                self.habilitar_opc_modificar_evento()
                continue
            # Si es una acción final, guardar y salir del loop
            if event in ("Confirmar evento", "Rechazar evento", "Solicitar revisión a experto"):
                accion_seleccionada = event
                break
        window.close()
        
        # Si se seleccionó una acción final, procesarla según el diagrama de secuencia
        if accion_seleccionada:
            self.tomar_selecc_opc_accion(accion_seleccionada)
    

    def tomar_selecc_opc_accion(self, accion):
        """
        Procesa la acción seleccionada por el usuario: valida los datos y cambia el estado del evento.
        Según el diagrama de secuencia, este método valida y luego llama a cambiar_estado_evento_sismico.
        """
        # Validar la acción seleccionada
        valido, mensaje = self.gestor_sismo.tomar_selecc_opc_accion(accion)
        if not valido:
            sg.popup(mensaje)
            return
        
        # Cambiar el estado del evento
        self.gestor_sismo.cambiar_estado_evento_sismico(self.gestor_sismo.evento_seleccionado, accion)
        
        # Mostrar confirmación
        if accion == "Confirmar evento":
            sg.popup("Evento confirmado. Estado actualizado y responsable registrado.")
        elif accion == "Rechazar evento":
            sg.popup("Evento rechazado. Estado actualizado y responsable registrado.")
        elif accion == "Solicitar revisión a experto":
            sg.popup("Revisión a experto solicitada. Estado actualizado y responsable registrado.")

    def habilitar_opc_mapa(self):
        sg.popup("Opción de mapa habilitada para el evento seleccionado. Acá se mostraría el mapa con la ubicación del evento y estaciones asociadas")

    def habilitar_opc_modificar_evento(self):
        sg.popup("Opción para modificar los datos del evento sísmico habilitada. Acá se permitiría editar los datos del evento seleccionado.")
