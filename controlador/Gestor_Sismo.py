class GestorSismo:
    def _init_(self):
        self.eventos_sismicos = []

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)

    def buscarEventosParaRevisar(self):
        eventos_pte_revision = []
        for evento in self.eventos_sismicos:
            if evento.buscarEventosParaRevisar():
                eventos_pte_revision.append(evento)
        return eventos_pte_revision

    def bloquearEvento(self, evento):
        evento.bloquear()
        print(f"Evento {evento.getFechaHoraOcurrencia()} bloqueado.")

    def rechazarEvento(self, evento):
        evento.rechazar()
        print(f"Evento {evento.getFechaHoraOcurrencia()} rechazado.")