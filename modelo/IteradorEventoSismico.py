from typing import Any, List, Callable
from .IIterador import IIterador

class IteradorEventoSismico(IIterador):
    def __init__(self, eventos_sismicos):
        self._eventos_sismicos = eventos_sismicos
        self._posicion_actual = 0

    def elemento_actual(self) -> Any:
        if 0 <= self._posicion_actual < len(self._eventos_sismicos):
            return self._eventos_sismicos[self._posicion_actual]
        return None

    def comprobar_filtro(self, filtros: List[Callable]) -> bool:
        """
        Comprueba si el evento actual cumple con todos los filtros especificados.
        Los filtros son funciones que reciben un evento y retornan True/False.
        Si no se pasan filtros, retorna True (sin filtrar).
        """
        evento_actual = self.elemento_actual()
        if evento_actual is None:
            return False
        
        # Si no hay filtros, aceptar todos los eventos
        if not filtros:
            return True
        
        # Aplicar todos los filtros - todos deben retornar True
        for filtro in filtros:
            if not filtro(evento_actual):
                return False
        return True

    def ha_finalizado(self) -> bool:
        return self._posicion_actual >= len(self._eventos_sismicos)

    def primero(self) -> None:
        self._posicion_actual = 0

    def siguiente(self) -> None:
        self._posicion_actual += 1

    def __iter__(self):
        return self
    
    

