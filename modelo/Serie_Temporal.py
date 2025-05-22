class SerieTemporal:
    def __init__(self, condicion_alarma, fecha_hora_inicio_registro_muestras, fecha_hora_registro, frecuencia_muestreo):
        self.condicion_alarma =  condicion_alarma
        self.fecha_hora_inicio_registro_muestras = fecha_hora_inicio_registro_muestras
        self.fechaHora_registro = fecha_hora_registro
        self.frecuencia_muestreo = frecuencia_muestreo
