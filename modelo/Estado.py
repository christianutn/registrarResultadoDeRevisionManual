class Estado:
    def __init__(self, nombre_estado):
        self.nombre_estado = nombre_estado

    def esPteRevision(self):
        return self.nombre_estado == "pendiente_revision"


# Función fuera de la clase para inicializar estados mock

def inicializar_estados_mock():
    return [
        Estado("auto_detectado"),
        Estado("pendiente_revision"),
        Estado("bloqueado"),
        Estado("rechazado")
    ]