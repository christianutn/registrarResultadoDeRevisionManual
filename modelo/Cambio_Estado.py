from datetime import datetime
from .Estado import Estado

class CambioEstado:
    def __init__(self, fecha_hora_inicio: datetime, estado: Estado, empleado):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = None
        self.estado = estado
        self.empleado = empleado

    def esActual(self) -> bool:
        return self.fecha_hora_fin is None

    def es_pte_revision(self) -> bool:
        return self.estado.es_pte_revision()
    
    def es_auto_detectado(self) -> bool:
        return self.estado.es_auto_detectado()

    def set_fecha_hora_fin(self, fecha_hora):
        self.fecha_hora_fin = fecha_hora
    