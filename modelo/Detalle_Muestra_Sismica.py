class DetalleMuestraSismica:
    def __init__(self, valor):
        self.valor = valor
        self.tipo_de_dato = None               

    def set_tipo_de_dato(self, tipo_de_dato):
        self.tipo_de_dato = tipo_de_dato
        
        
    def get_datos(self):
        return self.tipo_de_dato.get_denominacion(), self.valor