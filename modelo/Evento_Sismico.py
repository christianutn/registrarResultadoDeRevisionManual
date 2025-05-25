from .Cambio_Estado import CambioEstado

class EventoSismico:
    def __init__(self, fecha_hora_ocurrencia, latitud_epicentro, latitud_hipocentro, longitud_epicentro, longitud_hipocentro, valor_magnitud):
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
        self.cambio_estado = []
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
        estado_actual.set_fecha_hora_fin(hora_actual)
        nuevo_estado = CambioEstado(hora_actual, estado_recuperado, empleado)
        self.cambio_estado.append(nuevo_estado)

    def obtener_datos_evento_sismico(self):
        return {
            "fecha_hora_ocurrencia": self.fecha_hora_ocurrencia,
            "latitud_epicentro": self.latitud_epicentro,
            "longitud_epicentro": self.longitud_epicentro,
            "latitud_hipocentro": self.latitud_hipocentro,
            "longitud_hipocentro": self.longitud_hipocentro,
            "valor_magnitud": self.valor_magnitud
            # "alcance_sismo": self.alcance_sismo.get_descripcion() if self.alcance_sismo else None,
            # "origen_generacion": self.origen_de_generacion.get_nombre() if self.origen_de_generacion else None,
            # "estado_actual": self.esActual().estado.nombre_estado if self.esActual() else "N/A"
        }

    def obtener_series_temporales(self):
        return self.series_temporales

    def agregar_serie_temporal(self, serie):
        self.series_temporales.append(serie)

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
    
    
