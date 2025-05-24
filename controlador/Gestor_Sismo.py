class GestorSismo:
    def __init__(self):
        self.eventos_sismicos = []

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)

    def buscar_eventos_para_revisar(self):
        eventos_para_revisar = []
        for evento in self.eventos_sismicos:
            if evento.buscar_eventos_para_revisar():
                eventos_para_revisar.append(evento)
        return eventos_para_revisar

    def bloquear_evento(self, evento):
        evento.bloquear()
        print(f"Evento {evento.getFechaHoraOcurrencia()} bloqueado.")

    def rechazar_evento(self, evento):
        evento.rechazar()
        print(f"Evento {evento.getFechaHoraOcurrencia()} rechazado.")
    
    def registrarResRevManual(self):
        # Llama al método que busca los eventos para revisar
        return self.buscar_eventos_para_revisar()