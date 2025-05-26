class SerieTemporal:
    def __init__(self, condicion_alarma, fecha_hora_inicio_registro_muestras, fecha_hora_registro, frecuencia_muestreo):
        self.condicion_alarma =  condicion_alarma
        self.fecha_hora_inicio_registro_muestras = fecha_hora_inicio_registro_muestras
        self.fechaHora_registro = fecha_hora_registro
        self.frecuencia_muestreo = frecuencia_muestreo
        self.muestras_sismicas = [] 
        self.sismografo = None
        
    def agregar_muestra_sismica(self, muestra_sismica):
        self.muestras_sismicas.append(muestra_sismica)
        
    def set_sismografo(self, sismografo):
        self.sismografo = sismografo
        
    def get_datos(self):
        datos_muestras = []
        for i in range(len(self.muestras_sismicas)):
            datos_muestras.append(self.muestras_sismicas[i].get_datos())
        estacion_codigo, estacion_nombre = self.sismografo.get_datos_estacion()
        return datos_muestras, estacion_codigo, estacion_nombre
    
    
        
       