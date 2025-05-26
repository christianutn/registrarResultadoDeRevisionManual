class MuestraSismica:
    def __init__(self, fecha_hora_muestra):
        self.fecha_hora_muestra = fecha_hora_muestra
        self.detalles_muestra_sismica = [] 
    
    def agregar_detalle_muestra(self, detalle_muestra):
        self.detalles_muestra_sismica.append(detalle_muestra)
        
        
    def get_datos(self):
        datos_detalles = []
        for detalle in self.detalles_muestra_sismica:
            datos_detalles.append(detalle.get_datos())
        return datos_detalles