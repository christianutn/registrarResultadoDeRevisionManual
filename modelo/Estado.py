class Estado:
    def __init__(self, nombre_estado):
        self.nombre_estado = nombre_estado

    def es_pte_revision(self):
        if self.nombre_estado == "pendiente_revision":
            return True
        return False
    
    def es_auto_detectado(self):
        if self.nombre_estado == "auto_detectado":
            return True
        return False
       

# Función fuera de la clase para inicializar estados mock

def inicializar_estados_mock():
    return [
        Estado("auto_detectado"),
        Estado("pendiente_revision"),
        Estado("bloqueado"),
        Estado("rechazado")
    ]