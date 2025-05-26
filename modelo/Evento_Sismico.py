from .Cambio_Estado import CambioEstado
from .Clasificacion_Sismo import inicializar_clasificaciones_mock
from .Origen_De_Generacion import inicializar_origenes_mock
from .Alcance_Sismo import inicializar_alcances_mock

class EventoSismico:
    def __init__(self, fecha_hora_ocurrencia, latitud_epicentro, latitud_hipocentro, longitud_epicentro, longitud_hipocentro, valor_magnitud,  cambio_estado):
        self.fecha_hora_ocurrencia =  fecha_hora_ocurrencia
        self.latitud_epicentro = latitud_epicentro
        self.latitud_hipocentro = latitud_hipocentro
        self.longitud_epicentro = longitud_epicentro
        self.longitud_hipocentro =  longitud_hipocentro
        self.valor_magnitud = valor_magnitud
        self.origen_de_generacion = None
        self.clasificacion_sismo = None
        self.alcance_sismo = None
        self.series_temporales = []
        self.cambio_estado = cambio_estado
        self.estado_actual = None

    def get_fecha_hora_ocurrencia(self):
        return self.fecha_hora_ocurrencia

    def get_latitud_epicentro(self):
        return self.latitud_epicentro

    def get_longitud_epicentro(self):
        return self.longitud_epicentro

    def get_latitud_hipocentro(self):
        return self.latitud_hipocentro

    def get_longitud_hipocentro(self):
        return self.longitud_hipocentro

    def get_estado_actual(self):   
        return self.estado_actual

    def bloquear(self, estado_recuperado, hora_actual, empleado):
        estado_actual = self.get_estado_actual()
        self.crear_cambio_estado(hora_actual, empleado, estado_actual, estado_recuperado)


    def crear_cambio_estado(self, hora_actual, empleado, estado_actual, estado_recuperado):
        # Si hay un estado actual, se le setea la fecha de fin
        if estado_actual is not None:
            estado_actual.set_fecha_hora_fin(hora_actual)
        # Crear el nuevo cambio de estado con la hora actual, el estado (puntero) y el empleado
        nuevo_cambio_estado = CambioEstado(hora_actual, estado_recuperado, empleado)
        self.cambio_estado.append(nuevo_cambio_estado)
        self.estado_actual = nuevo_cambio_estado


    def obtener_datos_evento_sismico(self):
        return {
            "fecha_hora_ocurrencia": self.fecha_hora_ocurrencia,
            "latitud_epicentro": self.latitud_epicentro,
            "longitud_epicentro": self.longitud_epicentro,
            "latitud_hipocentro": self.latitud_hipocentro,
            "longitud_hipocentro": self.longitud_hipocentro,
            "valor_magnitud": self.valor_magnitud
            
        }
        
    def obtener_datos_evento(self):
        return {
            "alcance_sismo": self.alcance_sismo.get_nombre() if self.alcance_sismo else None,
            "origen_generacion": self.origen_de_generacion.get_nombre() if self.origen_de_generacion else None,
            "clasificacion_sismo": self.clasificacion_sismo.get_nombre() if self.clasificacion_sismo else None,     
        }



    def agregar_cambio_estado(self, cambio):
        self.cambios_estado.append(cambio)

    def buscar_datos_evento_sismico(self):
        return self.obtener_datos_evento()

    def buscar_eventos_para_revisar(self):
        for ce in self.cambio_estado:
            if ce.esActual():
                self.estado_actual = ce
                if ce.es_pte_revision() or ce.es_auto_detectado():
                    return True
        return False

    def validar_y_asignar_clasificacion(self, clasificacion):
        self.clasificacion_sismo = next((c for c in inicializar_clasificaciones_mock() if c.get_nombre() == clasificacion), None)

    def validar_y_asignar_origen(self, origen):
        self.origen_de_generacion = next((o for o in inicializar_origenes_mock() if o.get_nombre() == origen), None)

    def validar_y_asignar_alcance(self, alcance):
        self.alcance_sismo = next((a for a in inicializar_alcances_mock() if a.get_nombre() == alcance), None)

    def set_clasificacion_sismo(self, clasificacion):
        self.validar_y_asignar_clasificacion(clasificacion)

    def set_origen_de_generacion(self, origen):
        self.validar_y_asignar_origen(origen)

    def set_alcance_sismo(self, alcance):
        self.validar_y_asignar_alcance(alcance)

    def obtener_series_temporales(self):
        datos_series = []
        for i in range(len(self.series_temporales)):
            datos_series.append(self.series_temporales[i].get_datos())
        return datos_series
        
    def agregar_serie_temporal(self, serie):
        self.series_temporales.append(serie)

