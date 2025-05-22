from datetime import datetime

class CambioEstado:
    def __init__(self, fechaHoraInicio: datetime, estado: Estado):
        self.__fechaHoraInicio= fechaHoraInicio
        self.__fechaHoraFin = None
        self.__estado = estado

    def esActual(self) -> bool:
        """
        Retorna True si el cambio está activo (sin fecha de fin).
        """
        return self.__fechaHoraFin is None

    def esPteRevision(self) -> bool:
        """
        Pregunta al objeto Estado si está pendiente de revisión.
        """
        return self.__estado.esPteRevision()

    def setFechaHoraFin(self, fecha_hora: datetime) -> None:
        self.__fechaHoraFin = fecha_hora

    @classmethod
    def new(cls, estado: Estado) -> 'CambioEstado':
        """
        Crea una nueva instancia con fecha de inicio actual.
        """
        return cls(datetime.now(), estado)
