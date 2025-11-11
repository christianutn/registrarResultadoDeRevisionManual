from typing import Any
from .IIterador import IIterador

class IteradorEventoSismico(IIterador):
    """
    Iterador concreto que recorre una colección de eventos sísmicos.
    Implementa el patrón Iterator permitando filtrar eventos según criterios específicos.
    El filtro se aplica internamente (self) según el diagrama de secuencia.
    """
    def __init__(self, eventos_sismicos):
        self._eventos_sismicos = eventos_sismicos
        self._posicion_actual = 0

    def elemento_actual(self) -> Any:
        """
        Retorna el evento actual en la posición del iterador si cumple el filtro.
        Aplica comprobar_filtro() internamente (llamada self).
        Retorna None si no hay elemento o no cumple el filtro.
        """
        if 0 <= self._posicion_actual < len(self._eventos_sismicos):
            evento = self._eventos_sismicos[self._posicion_actual]
            # Llamada interna (self) - consistente con el diagrama de secuencia
            if self.comprobar_filtro(evento):
                return evento
        return None

    def comprobar_filtro(self, evento) -> bool:
            # Delegar al evento la responsabilidad de saber si cumple el filtro (PATRÓN EXPERTO)
        return evento.es_pendiente_o_autodetectado()
        

    def ha_finalizado(self) -> bool:
        """
        Indica si el iterador ha recorrido todos los elementos.
        """
        return self._posicion_actual >= len(self._eventos_sismicos)

    def primero(self) -> None:
        """
        Posiciona el iterador en el primer elemento.
        """
        self._posicion_actual = 0

    def siguiente(self) -> None:
        """
        Avanza el iterador al siguiente elemento.
        """
        self._posicion_actual += 1

    def __iter__(self):
        """
        Soporte para iteración con Python (opcional).
        """
        return self
    
    

