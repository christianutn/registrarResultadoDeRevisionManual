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
        self.cambios_estado = None
        

        def agregar_serie_temporal(self, serie_temporal):
            self.series_temporales.append(serie_temporal)
        def obtener_series_temporales(self):
            return self.series_temporales
