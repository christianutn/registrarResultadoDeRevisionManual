from modelo.Usuario import Usuario 

class Sesion:
    def __init__(self, fecha_hora_inicio, fecha_hora_fin, usuario):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.usuario = usuario
        
    def set_usuario(self, usuario):
        self.usuario = usuario
        
    def obtener_empleado(self):
        return self.usuario.get_empleado()
    
def inicializar_actual_sesion():
    return Sesion(fecha_hora_fin=None, fecha_hora_inicio=None)