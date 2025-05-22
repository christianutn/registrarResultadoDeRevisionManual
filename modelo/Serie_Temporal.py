class SerieTemporal:
    def init(self, condicion_alarma, fecha_hora_inicio_registro_muestras, fecha_hora_registro, frecuencia_muestreo):
        self.condicionAlarma =  condicion_alarma
        self.fechaHoraInicioRegistroMuestras = fecha_hora_inicio_registro_muestras
        self.fechaHoraRegistro = fecha_hora_registro
        self.frecuenciaMuestreo = frecuencia_muestreo
