from datetime import datetime
from modelo.Estado import inicializar_estados_mock
from modelo.Sesion import Sesion

class GestorSismo:
    def __init__(self, sesion):
        self.eventos_sismicos = []
        self.sesion = sesion
        self.evento_seleccionado = None

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)
    
    def registrarResRevManual(self):
        # Llama al método que busca los datos de los eventos para revisar ordenados
        eventos_para_revisar = self.buscar_eventos_para_revisar()
        datos_eventos_para_revisar = self.buscar_datos_eventos_para_revisar(eventos_para_revisar)
        datos_eventos_ordenados = self.ordenar_eventos_fecha_hora_ocurrencia(datos_eventos_para_revisar)
        return datos_eventos_ordenados, eventos_para_revisar
        
    
    def buscar_datos_eventos_para_revisar(self, eventos_para_revisar): # GESTOR DEBE TENER ESTE MÉTODO 
        datos_eventos = [evento.obtener_datos_evento_sismico() for evento in eventos_para_revisar]
        return datos_eventos
    
    def buscar_eventos_para_revisar(self):
        eventos_para_revisar = []
        for evento in self.eventos_sismicos:
            if evento.buscar_eventos_para_revisar():
                eventos_para_revisar.append(evento)
        return eventos_para_revisar

    def ordenar_eventos_fecha_hora_ocurrencia(self, datos_eventos):
        # Ordena los datos por fecha y hora de ocurrencia usando un bucle for
        for i in range(len(datos_eventos)):
            for j in range(0, len(datos_eventos) - i - 1):
                if datos_eventos[j]["fecha_hora_ocurrencia"] > datos_eventos[j + 1]["fecha_hora_ocurrencia"]:
                    datos_eventos[j], datos_eventos[j + 1] = datos_eventos[j + 1], datos_eventos[j]
        return datos_eventos
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        self.cambiar_estado_evento_sismico(evento_seleccionado, accion)
        
        
    def cambiar_estado_evento_sismico(self, evento_seleccionado, accion):
        hora_actual = self.get_fecha_hora_actual()
        estados = inicializar_estados_mock()
        estado_recuperado = None
        
        for estado in estados:
            if estado.esBloqueado() and estado.esAmbitoEventoSismico():
                estado_recuperado = estado
                break
                
        empleado_logueado = self.buscar_usuario_logueado()
        # print(f"Empleado logueado: {empleado_logueado}")
        evento_seleccionado.bloquear(estado_recuperado, hora_actual, empleado_logueado)
        self.evento_seleccionado = evento_seleccionado
        
    
    def buscar_usuario_logueado(self):
        if self.sesion:
            return self.sesion.obtener_empleado()
        return None
        
        
    def get_fecha_hora_actual(self):
        return datetime.now()
    
    def buscar_datos_evento(self):
        datos_eventos = self.evento_seleccionado.obtener_datos_evento() 
        return datos_eventos
    
    def buscar_datos_series_temporales(self):
        datos_series_temporales = self.evento_seleccionado.obtener_series_temporales()
        datos_series_temporales_clasificados = self.clasificar_por_estacion(datos_series_temporales)
        return datos_series_temporales_clasificados
    
    def clasificar_por_estacion(self, datos_series_temporales):
        series_por_estacion = {}
        for serie in datos_series_temporales:
            nombre_estacion = serie[2] if len(serie) > 2 else 'SIN_NOMBRE'
            if nombre_estacion not in series_por_estacion:
                series_por_estacion[nombre_estacion] = []
            series_por_estacion[nombre_estacion].append(serie)
        return series_por_estacion

