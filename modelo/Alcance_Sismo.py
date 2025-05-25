class AlcanceSismo:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion


# Función para inicializar alcances de sismos

def inicializar_alcances_mock():
    return [
        AlcanceSismo("Sismo local", "Distancia epicentral hasta 100 km"),
        AlcanceSismo("Sismo regional", "Distancia epicentral entre 101 y 1000 km"),
        AlcanceSismo("Tele sismo", "Distancia epicentral mayor a 1000 km")
    ]