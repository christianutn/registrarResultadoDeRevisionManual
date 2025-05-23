from datetime import datetime

class CambioEstado:
    def __init__(self, fecha_hora_inicio: datetime, estado: Estado):
        self.__fecha_hora_inicio = fecha_hora_inicio
        self.__fecha_hora_fin = None
        self.__estado = estado

    def esActual(self) -> bool:
        """
        Retorna True si el cambio está activo (sin fecha de fin).
        """
        return self.__fecha_hora_fin is None

    def esPteRevision(self) -> bool:
        return self.estado.esPteRevision()

    def setFechaHoraFin(self, fecha_hora: datetime) -> None:
        self.fecha_hora_fin = fecha_hora

    @classmethod
    def new(cls, estado: Estado) -> 'CambioEstado':
        """
        Crea una nueva instancia con fecha de inicio actual.
        """
        return cls(datetime.now(), estado)
