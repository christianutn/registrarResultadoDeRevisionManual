import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controlador.Gestor_Sismo import GestorSismo
from interfaz.dialogs_ui import (
    EventSelectorDialog, 
    EventDetailsDialog, 
    mostrar_mensaje_informativo,
    mostrar_mensaje_error
)
from PySide6.QtWidgets import QDialog, QMessageBox


class PantallaAdmSismo:
    """
    Clase controladora de la pantalla de administración de sismos.
    Maneja la lógica de negocio y coordina con los diálogos UI para la presentación.
    """
    
    def __init__(self, gestor_sismo):
        self.gestor_sismo = gestor_sismo
        
    def opc_res_rev_manual(self):
        """Inicia el proceso de revisión manual de eventos sísmicos"""
        self.habilitarVentana()

    def habilitarVentana(self):
        """Habilita la ventana de selección de eventos sísmicos"""
        datos_eventos_ordenados, eventos_objetos = self.gestor_sismo.registrarResRevManual()
        self.solicitar_elecc_evento_sismico(datos_eventos_ordenados, eventos_objetos)

    def solicitar_elecc_evento_sismico(self, datos_eventos_ordenados, eventos_objetos):
        """
        Solicita al usuario la selección de un evento sísmico de la lista.
        
        Args:
            datos_eventos_ordenados: Lista de diccionarios con datos de eventos
            eventos_objetos: Lista de objetos EventoSismico correspondientes
        """
        if not datos_eventos_ordenados:
            mostrar_mensaje_informativo(
                "ℹ️ Información", 
                "No hay eventos pendientes de revisión en este momento."
            )
            return None, None
        
        # Crear el diálogo
        dialog = EventSelectorDialog(datos_eventos_ordenados, eventos_objetos)
        result = dialog.exec()
        
        if result == QDialog.Accepted and dialog.evento_seleccionado is not None:
            self.tomar_elecc_evento_sismico(dialog.evento_seleccionado, "Seleccionar")
        else:
            self.tomar_elecc_evento_sismico(None, "Cancelar")
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        """
        Procesa la elección del evento sísmico seleccionado por el usuario.
        
        Args:
            evento_seleccionado: El objeto EventoSismico seleccionado
            accion: La acción a realizar ("Seleccionar" o "Cancelar")
        """
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
        """
        Muestra los datos detallados del evento seleccionado y sus series temporales.
        Construye el texto formateado y delega la presentación al diálogo UI.
        """
        datos_evento = self.gestor_sismo.buscar_datos_evento()
        datos_series = self.gestor_sismo.buscar_datos_series_temporales()
        print("Datos del evento y series temporales obtenidos exitosamente")
        
        # Construir texto para datos del evento
        texto_evento = self._construir_texto_evento(datos_evento)
        
        # Construir texto para series temporales
        texto_series = self._construir_texto_series(datos_series)

        # Crear el diálogo de detalles
        dialog = EventDetailsDialog(texto_evento, texto_series, self)
        dialog.exec()
    
    def _construir_texto_evento(self, datos_evento):
        """
        Construye el texto formateado con la información del evento.
        
        Args:
            datos_evento: Diccionario con los datos del evento
            
        Returns:
            str: Texto formateado con la información del evento
        """
        texto = "📊 INFORMACIÓN DEL EVENTO SÍSMICO\n"
        texto += "=" * 50 + "\n\n"
        
        if isinstance(datos_evento, dict):
            texto += f"📍 Alcance: {datos_evento.get('alcance_sismo', 'N/D')}\n"
            texto += f"🌋 Origen: {datos_evento.get('origen_generacion', 'N/D')}\n"
            texto += f"📐 Clasificación: {datos_evento.get('clasificacion_sismo', 'N/D')}\n"
        else:
            texto += str(datos_evento) + "\n"
        
        return texto
    
    def _construir_texto_series(self, datos_series):
        """
        Construye el texto formateado con las series temporales.
        
        Args:
            datos_series: Diccionario con las series temporales por estación
            
        Returns:
            str: Texto formateado con las series temporales
        """
        texto = "\n\n📡 SERIES TEMPORALES POR ESTACIÓN\n"
        texto += "=" * 50 + "\n"
        
        if isinstance(datos_series, dict):
            for estacion, series in datos_series.items():
                texto += f"\n🏢 Estación: {estacion}\n"
                texto += "-" * 40 + "\n"
                for serie in series:
                    try:
                        muestras = serie[0]
                        codigo = serie[1]
                        nombre = serie[2]
                    except Exception:
                        texto += f"  Serie: {serie}\n"
                        continue
                    
                    texto += f"  📟 Código: {codigo} | Nombre: {nombre}\n"
                    texto += f"  📊 Cantidad de muestras: {len(muestras) if hasattr(muestras, '__len__') else 'N/D'}\n"
                    
                    # Mostrar hasta 2 ejemplos de muestras por serie
                    if hasattr(muestras, '__iter__'):
                        for i, muestra in enumerate(list(muestras)[:2]):
                            texto += f"    • Ejemplo muestra {i+1}: {muestra}\n"
        else:
            texto += str(datos_series)
        
        return texto

    def tomar_selecc_opc_accion(self, accion):
        """
        Procesa la acción seleccionada por el usuario: valida los datos y cambia el estado del evento.
        Según el diagrama de secuencia, este método valida y luego llama a cambiar_estado_evento_sismico.
        
        Args:
            accion: La acción seleccionada ("Confirmar evento", "Rechazar evento", etc.)
        """
        # Validar la acción seleccionada
        valido, mensaje = self.gestor_sismo.tomar_selecc_opc_accion(accion)
        if not valido:
            mostrar_mensaje_error(
                "⚠️ Error de Validación", 
                f"⚠️ Validación Fallida\n\n{mensaje}"
            )
            return
        
        # Cambiar el estado del evento
        self.gestor_sismo.cambiar_estado_evento_sismico(
            self.gestor_sismo.evento_seleccionado, 
            accion
        )
        
        # Mostrar confirmación según la acción
        self._mostrar_confirmacion_accion(accion)
    
    def _mostrar_confirmacion_accion(self, accion):
        """
        Muestra el mensaje de confirmación apropiado según la acción realizada.
        
        Args:
            accion: La acción que fue ejecutada
        """
        mensajes = {
            "Confirmar evento": (
                "✅ Confirmación Exitosa",
                "✅ Evento confirmado\n\nEstado actualizado y responsable registrado correctamente."
            ),
            "Rechazar evento": (
                "❌ Rechazo Registrado",
                "❌ Evento rechazado\n\nEstado actualizado y responsable registrado correctamente."
            ),
            "Solicitar revisión a experto": (
                "👨‍🔬 Solicitud Enviada",
                "👨‍🔬 Revisión a experto solicitada\n\nEstado actualizado y responsable registrado correctamente."
            )
        }
        
        if accion in mensajes:
            titulo, mensaje = mensajes[accion]
            mostrar_mensaje_informativo(titulo, mensaje)

    def habilitar_opc_mapa(self):
        """Habilita la opción de visualizar el mapa del evento sísmico"""
        mostrar_mensaje_informativo(
            "🗺️ Visualización de Mapa",
            "🗺️ Mapa del Evento Sísmico\n\nAquí se mostraría el mapa con la ubicación del evento\ny las estaciones sísmicas asociadas."
        )

    def habilitar_opc_modificar_evento(self):
        """Habilita la opción de modificar los datos del evento sísmico"""
        mostrar_mensaje_informativo(
            "✏️ Edición de Evento",
            "✏️ Modificar Evento Sísmico\n\nAquí se permitiría editar los datos del evento seleccionado\n(magnitud, coordenadas, clasificación, etc.)"
        )
