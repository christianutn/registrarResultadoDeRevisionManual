class Empleado:
    def __init__(self, apellido, mail, nombre, telefono, rol):
        self.apellido =  apellido
        self.mail = mail
        self.nombre = nombre
        self.telefono = telefono
        self.rol = None
        
    # def get_rol(self, descripcion_rol,nombre):
    #     self.descripcion_rol = descripcion_rol
    #     self.nombre = nombre