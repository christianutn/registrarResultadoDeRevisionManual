class Sismografo:
    def __init__(self, fecha_adquisicion, identificador_sismografo, nro_serie):
        self.fecha_adquisicion = fecha_adquisicion
        self.identificor_sismografo = identificador_sismografo
        self.nro_serie = nro_serie
        self.estacion_sismologica = None
        self.series_temporales = [] 
        
        def agregar_serie_temporal(self, serie_temporal):
            self.series_temporales.append(serie_temporal)
