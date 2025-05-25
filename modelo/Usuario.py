from modelo.Empleado import Empleado

class Usuario:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        self.empleado = None
        
        
    def set_empleado(self, empleado):
        self.empleado = empleado
        
    def get_nombre(self):
        return Empleado.get_empleado(self.empleado)