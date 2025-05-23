class Estado:
    def __init__(self, ambito, nombre_estado, es_bloqueado, es_rechazado):
        self.ambito = ambito
        self.nombreEstado = nombre_estado
        self.esBloqueado = es_bloqueado
        self.esRechazado = es_rechazado

    def esPteRevision(self) -> bool:
        return self.nombre_estado == "pendiente_revision"