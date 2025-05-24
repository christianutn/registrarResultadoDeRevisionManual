class Sesion:
    def __init__(self, fecha_hora_inicio, fecha_hora_fin):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.usuario = None
        
    def set_usuario(self, usuario):
        self.usuario = usuario