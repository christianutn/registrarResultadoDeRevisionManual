class AlcanceSismo:
    """
    Representa el alcance de un sismo, con su nombre y descripción.
    """

    def __init__(self, nombre: str, descripcion: str):
        self.__nombre = nombre
        self.__descripcion = descripcion

    def getNombre(self) -> str:
        """
        Devuelve el nombre del alcance del sismo.
        """
        return self.__nombre
    
    def getDescripcion(self) -> str:
        """
        Devuelve el nombre del alcance del sismo.
        """
        return self.__descripcion

    def mostrarDatos(self) -> str:
        """
        Devuelve un string con los datos del alcance.
        """
        return f"Nombre: {self.__nombre}, Descripción: {self.__descripcion}"
