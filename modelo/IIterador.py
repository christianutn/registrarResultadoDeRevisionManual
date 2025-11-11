from typing import Any, List

class IIterador:
    def elemento_actual(self) -> Any:
        raise NotImplementedError

    def comprobar_filtro(self, filtros: List[Any]) -> bool:
        raise NotImplementedError

    def ha_finalizado(self) -> bool:
        raise NotImplementedError

    def primero(self) -> None:
        raise NotImplementedError

    def siguiente(self) -> None:
        raise NotImplementedError