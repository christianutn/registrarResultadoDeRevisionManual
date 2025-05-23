class GestorSismo:
    def __init__(self):
        self.eventos_sismicos = []

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)

    def buscar_eventos_para_revisar(self):
        eventos_pte_revision = []
        for evento in self.eventos_sismicos:
            if evento.buscar_eventos_para_revisar():
                eventos_pte_revision.append(evento)
        return eventos_pte_revision

    def bloquear_evento(self, evento):
        evento.bloquear()
        print(f"Evento {evento.getFechaHoraOcurrencia()} bloqueado.")

    def rechazar_evento(self, evento):
        evento.rechazar()
        print(f"Evento {evento.getFechaHoraOcurrencia()} rechazado.")