from datetime import datetime
from .Estado import Estado

class CambioEstado:
    def __init__(self, fecha_hora_inicio: datetime, estado: Estado):
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = None
        self.estado = estado

    def esActual(self) -> bool:
        """
        Retorna True si el cambio está activo (sin fecha de fin).
        """
        return self.fecha_hora_fin is None

    def es_pte_revision(self) -> bool:
        return self.estado.es_pte_revision()
    
    def es_auto_detectado(self) -> bool:
        return self.estado.es_auto_detectado()

    def setFechaHoraFin(self, fecha_hora: datetime) -> None:
        self.fecha_hora_fin = fecha_hora
    

    @classmethod
    def new(cls, estado: Estado) -> 'CambioEstado':
        """
        Crea una nueva instancia con fecha de inicio actual.
        """
        return cls(datetime.now(), estado)

    @classmethod
    def crear(cls, nombre_estado):
        from .Estado import Estado
        estado = Estado(nombre_estado)
        return cls(datetime.now(), estado)
