from datetime import datetime
from modelo.Estado import Estado

class GestorSismo:
    def __init__(self):
        self.eventos_sismicos = []
        self.sesion = None

    def agregarEvento(self, evento):
        self.eventos_sismicos.append(evento)

    def bloquear_evento(self, evento):
        evento.bloquear()
        print(f"Evento {evento.getFechaHoraOcurrencia()} bloqueado.")

    def rechazar_evento(self, evento):
        evento.rechazar()
        print(f"Evento {evento.getFechaHoraOcurrencia()} rechazado.")
    
    def registrarResRevManual(self):
        # Llama al método que busca los datos de los eventos para revisar ordenados
        eventos_para_revisar = self.buscar_eventos_para_revisar()
        datos_eventos_para_revisar = self.buscar_datos_eventos_para_revisar(eventos_para_revisar)
        datos_eventos_ordenados = self.ordenar_eventos_fecha_hora_ocurrencia(datos_eventos_para_revisar)
        return datos_eventos_ordenados
        
    
    def buscar_datos_eventos_para_revisar(self, eventos_para_revisar): # GESTOR DEBE TENER ESTE MÉTODO 
        datos_eventos = [evento.obtener_datos_evento_sismico() for evento in eventos_para_revisar]
        return datos_eventos
    
    def buscar_eventos_para_revisar(self):
        eventos_para_revisar = []
        for evento in self.eventos_sismicos:
            if evento.buscar_eventos_para_revisar():
                eventos_para_revisar.append(evento)
        return eventos_para_revisar

    def ordenar_eventos_fecha_hora_ocurrencia(self, datos_eventos):
        # Ordena los datos por fecha y hora de ocurrencia usando un bucle for
        for i in range(len(datos_eventos)):
            for j in range(0, len(datos_eventos) - i - 1):
                if datos_eventos[j]["fecha_hora_ocurrencia"] > datos_eventos[j + 1]["fecha_hora_ocurrencia"]:
                    datos_eventos[j], datos_eventos[j + 1] = datos_eventos[j + 1], datos_eventos[j]
        return datos_eventos
    
    def tomar_elecc_evento_sismico(self, evento_seleccionado, accion):
        self.cambiar_estado_evento_sismico(evento_seleccionado, accion)
        
    def cambiar_estado_evento_sismico(self, evento_seleccionado, accion):
        hora_actual = self.get_fecha_hora_actual()
        estados = Estado.inicializar_estados_mock()
        print(estados)
        estado_recuperado = None
        
        for estado in estados:
            if estado.esBloqueado() and estado.esAmbitoEventoSismico():
                estado_recuperado = estado
                break
                
        usuario_logueado = self.buscar_usuario_logueado()
        if usuario_logueado is None:
            print("No hay usuario logueado para registrar el cambio de estado")
            return None
            
        empleado_logueado = usuario_logueado.empleado
        if empleado_logueado is None:
            print("El usuario no tiene un empleado asociado")
            return None
            
        # Aquí continuaremos con la lógica para cambiar el estado usando el estado_recuperado y el empleado_logueado
    
    def buscar_usuario_logueado(self):
        if self.sesion:
            return self.sesion.get_usuario_logueado()
        return None
        
        
        
    def get_fecha_hora_actual(self):
        return datetime.now()