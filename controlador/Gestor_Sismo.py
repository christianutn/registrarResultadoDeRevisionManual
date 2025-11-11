from datetime import datetime
from modelo.Estado import inicializar_estados_mock

# TODO: Cuando se implemente la capa de persistencia, considerar:
# from config.db import get_session
# from models.estado_model import EstadoModel

class GestorSismo:
    def __init__(self, sesion):
        self.eventos_sismicos = []
        self.sesion = sesion
        self.evento_seleccionado = None  
        self.empleado_logueado = None  

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)
    
    def registrarResRevManual(self):
        eventos_para_revisar = self.buscar_eventos_para_revisar()
        datos_eventos_para_revisar = self.buscar_datos_eventos_para_revisar(eventos_para_revisar)
        datos_eventos_ordenados = self.ordenar_eventos_fecha_hora_ocurrencia(datos_eventos_para_revisar)
        return datos_eventos_ordenados, eventos_para_revisar
        
    
    def buscar_datos_eventos_para_revisar(self, eventos_para_revisar): 
        datos_eventos = []
        for evento in eventos_para_revisar:
            datos_sismico = {}
            try:
                datos_sismico = evento.obtener_datos_evento_sismico() or {}
            except Exception:
                datos_sismico = {}
            datos_meta = {}
            try:
                datos_meta = evento.obtener_datos_evento() or {}
            except Exception:
                datos_meta = {}
            # fusiono datos sismicos con metadatos (alcance, origen, clasificacion)
            merged = {**datos_sismico, **datos_meta}
            datos_eventos.append(merged)
        return datos_eventos
    
    def buscar_eventos_para_revisar(self):
        # TODO: Reemplazar por consulta a base de datos:
        # db_session = get_session()
        # eventos_db = db_session.query(EventoSismicoModel).filter(
        #     EventoSismicoModel.estado.in_(['pendiente_revision', 'auto_detectado'])
        # ).all()
        # return [convertir_modelo_a_entidad(e) for e in eventos_db]
        
        eventos_para_revisar = []
        for evento in self.eventos_sismicos:
            if evento.buscar_eventos_para_revisar():
                eventos_para_revisar.append(evento)
        return eventos_para_revisar

    def ordenar_eventos_fecha_hora_ocurrencia(self, datos_eventos):
        for i in range(len(datos_eventos)):
            for j in range(0, len(datos_eventos) - i - 1):
                if datos_eventos[j]["fecha_hora_ocurrencia"] > datos_eventos[j + 1]["fecha_hora_ocurrencia"]:
                    datos_eventos[j], datos_eventos[j + 1] = datos_eventos[j + 1], datos_eventos[j]
        return datos_eventos
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        self.cambiar_estado_evento_sismico(evento_seleccionado, accion)

        
        
    def cambiar_estado_evento_sismico(self, evento_seleccionado, accion):
        hora_actual = self.get_fecha_hora_actual()
        
        # TODO: Considerar cargar estados desde BD si son configurables
        # Por ahora, los estados son datos de catálogo (mock está bien)
        estados = inicializar_estados_mock()
        estado_recuperado = None
        
        for estado in estados:
            if accion == "Rechazar evento":
                # cuando se rechaza, el sistema debe bloquear el evento (según el CU)
                if estado.esBloqueado() and estado.esAmbitoEventoSismico(): # PATRÓN EXPERTO 
                    estado_recuperado = estado
                    self.empleado_logueado = self.buscar_usuario_logueado() # PATRÓN EXPERTO
                    break
            elif accion == "Confirmar evento":
                if estado.esConfirmado() and estado.esAmbitoEventoSismico(): # PATRÓN EXPERTO 
                    estado_recuperado = estado
                    break
            elif accion == "Solicitar revisión a experto":
                # mapear solicitud de revisión a bloqueo para que un responsable asuma la revisión
                if estado.esBloqueado() and estado.esAmbitoEventoSismico():
                    estado_recuperado = estado
                    self.empleado_logueado = self.buscar_usuario_logueado()
                    break
            else:
                # otras acciones no cambian el estado
                estado_recuperado = None
                break
                
    
        if estado_recuperado is None:
            # no se encontró un estado aplicable -> no hacemos cambios
            return
        if estado_recuperado.nombre_estado == "rechazado":
            evento_seleccionado.rechazar(estado_recuperado, hora_actual, self.empleado_logueado)
        elif estado_recuperado.nombre_estado == "bloqueado":
            evento_seleccionado.bloquear(estado_recuperado, hora_actual, self.empleado_logueado)
        elif estado_recuperado.nombre_estado == "confirmado":
            evento_seleccionado.confirmar(estado_recuperado, hora_actual, self.empleado_logueado)
        
        self.evento_seleccionado = evento_seleccionado
        
    
    
    def buscar_usuario_logueado(self):
        if self.sesion:
            return self.sesion.obtener_empleado()
        return None
        
        
    def get_fecha_hora_actual(self):
        return datetime.now()
    
    def buscar_datos_evento(self): # PATRÓN CONTROLADOR
        datos_eventos = self.evento_seleccionado.obtener_datos_evento() 
        return datos_eventos
    
    def buscar_datos_series_temporales(self): # PATRÓN CONTROLADOR
        datos_series_temporales = self.evento_seleccionado.obtener_series_temporales()
        datos_series_temporales_clasificados = self.clasificar_por_estacion(datos_series_temporales)
        return datos_series_temporales_clasificados
    
    def clasificar_por_estacion(self, datos_series_temporales):
        series_por_estacion = {}
        for serie in datos_series_temporales:
            nombre_estacion = serie[2] if len(serie) > 2 else 'SIN NOMBRE'
            if nombre_estacion not in series_por_estacion:
                series_por_estacion[nombre_estacion] = []
            series_por_estacion[nombre_estacion].append(serie)
        return series_por_estacion
    
    def tomar_selecc_opc_accion(self, opcion):

        if not self.validar_selecc_opc(opcion):
            return False, "Debe seleccionar una acción válida."
        if not self.validar_existencia_datos():
            return False, "Faltan datos obligatorios: magnitud, alcance u origen de generación."
        return True, "Acción válida y datos completos."

    def validar_selecc_opc(self, opcion):
        return opcion in ["Confirmar evento", "Rechazar evento", "Solicitar revisión a experto"]

    def validar_existencia_datos(self):
        datos_sismico = self.evento_seleccionado.obtener_datos_evento_sismico()
        datos_evento = self.evento_seleccionado.obtener_datos_evento()
        return bool(
            datos_sismico.get("valor_magnitud") and
            datos_evento.get("alcance_sismo") and
            datos_evento.get("origen_generacion")
        )

