class ClasificacionSismo:
    def __init__(self, km_profundidad_desde, km_profundidad_hasta, nombre):
        self.km_profundidad_desde =  km_profundidad_desde
        self.km_profundidad_hasta = km_profundidad_hasta
        self.nombre = nombre
        
    def get_km_profundidad_desde(self):
        return self.km_profundidad_desde
    
    
    def get_km_profundidad_hasta(self):
        return self.km_profundidad_hasta    
    
    
    def get_nombre(self):   
        return self.nombre
    
    def set_km_profundidad_desde(self, km_profundidad_desde):
        self.km_profundidad_desde = km_profundidad_desde
        
        
    def set_km_profundidad_hasta(self, km_profundidad_hasta):
        self.km_profundidad_hasta = km_profundidad_hasta
        
    
    def set_nombre(self, nombre):
        self.nombre = nombre
    
