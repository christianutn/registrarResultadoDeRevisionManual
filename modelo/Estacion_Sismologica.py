class EstacionSismologica:
    def __init__(self, codigo_estacion, documento_certificacion_adq, fecha_solicitud_certificacion, latitud, longitud, nombre, nro_certificacion_adquisicion):
        self.codigo_estacion =  codigo_estacion
        self.documento_certificacion_adq = documento_certificacion_adq
        self.fecha_solicitud_certificacion = fecha_solicitud_certificacion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.nro_certificacion_adquisicion = nro_certificacion_adquisicion
