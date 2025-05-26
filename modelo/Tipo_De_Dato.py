class TipoDeDato:
    def __init__(self, denominacion, nombre_unidad_medida, valor_umbral):
        self.denominacion =  denominacion
        self.nombre_unidad_medida = nombre_unidad_medida
        self.valor_umbral = valor_umbral

    def get_denominacion(self):
        return self.denominacion   
    
    def get_nombre_unidad_medida(self):
        return self.nombre_unidad_medida