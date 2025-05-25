from modelo.Empleado import Empleado

class Usuario:
    def __init__(self, nombre, contraseña, empleado):
        self.nombre = nombre
        self.contraseña = contraseña
        self.empleado = empleado
        
        
    def set_empleado(self, empleado):
        self.empleado = empleado
        
    def get_empleado(self):
        return self.empleado.get_empleado()