class OrigenDeGeneracion:
    def __init__(self, descripcion, nombre):
        self.descripcion = descripcion
        self.nombre = nombre

    def get_descripcion(self):
        return self.descripcion

    def get_nombre(self):
        return self.nombre


def inicializar_origenes_mock():
    return [
        OrigenDeGeneracion("Sismo causado por interacción entre placas tectónicas", "Sismo interplaca"),
        OrigenDeGeneracion("Sismo causado por actividad volcánica", "Sismo volcánico"),
        OrigenDeGeneracion("Sismo causado por explosiones humanas", "Sismo por explosiones de minas")
    ]