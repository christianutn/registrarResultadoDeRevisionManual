class AlcanceSismo:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        
        
    def get_nombre(self):
        return self.nombre

        
    def get_descripcion(self):  
        return self.descripcion


    def set_nombre(self, nombre):
        self.nombre = nombre


    def set_descripcion(self, descripcion):
        self.descripcion = descripcion