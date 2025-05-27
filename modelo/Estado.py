class Estado:
    def __init__(self, nombre_estado, ambito):
        self.nombre_estado = nombre_estado
        self.ambito = ambito
        
        
    def es_pte_revision(self):
        if self.nombre_estado == "pendiente_revision":
            return True
        return False
    
    def es_auto_detectado(self):
        if self.nombre_estado == "auto_detectado":
            return True
        return False
    
    def esAmbitoEventoSismico(self):
        return self.ambito == "evento_sismico"
    
    def esBloqueado(self):
        if self.nombre_estado == "bloqueado":
            return True
        return False
    
    def esRechazado(self):
        if self.nombre_estado == "rechazado":
            return True
        return False
    
    def esConfirmado(self):
        if self.nombre_estado == "confirmado":
            return True
        return False



def inicializar_estados_mock():
    return [
        Estado("auto_detectado", "evento_sismico"),
        Estado("pendiente_revision", "evento_sismico"),
        Estado("bloqueado", "evento_sismico"),
        Estado("rechazado", "evento_sismico"),
        Estado("confirmado", "evento_sismico"),
        Estado("activo", "sismografo"),
        Estado("inactivo", "sismografo")
    ]