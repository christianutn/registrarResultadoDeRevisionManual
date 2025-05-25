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
    
    def buscar_datos_eventos_para_revisar(self):
        eventos = self.buscar_eventos_para_revisar()
        datos_eventos = [evento.obtener_datos_evento_sismico() for evento in eventos]
        return datos_eventos
    
    def ordenar_Eventos_Fecha_Hora_Ocurrencia(self):
        # Obtiene los datos de los eventos para revisar
        datos_eventos = self.buscar_datos_eventos_para_revisar()
        # Ordena los datos por fecha y hora de ocurrencia usando un bucle for
        for i in range(len(datos_eventos)):
            for j in range(0, len(datos_eventos) - i - 1):
                if datos_eventos[j]["fecha_hora_ocurrencia"] > datos_eventos[j + 1]["fecha_hora_ocurrencia"]:
                    datos_eventos[j], datos_eventos[j + 1] = datos_eventos[j + 1], datos_eventos[j]
        return datos_eventos