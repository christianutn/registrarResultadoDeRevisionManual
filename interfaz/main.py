import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controlador.Gestor_Sismo import GestorSismo
from interfaz.Pantalla_Adm_Sismo import PantallaAdmSismo
from interfaz.menu_opciones import mostrar_menu_opciones
from modelo.Sesion import Sesion
from modelo.Usuario import Usuario
from modelo.Empleado import Empleado
from modelo.Estado import inicializar_estados_mock
from datetime import datetime
import csv
import random
from modelo.Evento_Sismico import EventoSismico
from modelo.Cambio_Estado import CambioEstado

def cargar_eventos_desde_csv(ruta_csv):
    eventos = []
    estados_disponibles = inicializar_estados_mock()
    from modelo.Serie_Temporal import SerieTemporal
    from modelo.Muestra_Sismica import MuestraSismica
    from modelo.Detalle_Muestra_Sismica import DetalleMuestraSismica
    from modelo.Tipo_De_Dato import TipoDeDato
    from modelo.Estacion_Sismologica import EstacionSismologica
    from modelo.Sismografo import Sismografo
    from datetime import timedelta

    denominaciones = ["Velocidad de onda", "Frecuencia de onda", "Longitud"]
    unidades = ["km/seg", "Hz", "km/ciclo"]

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            evento = EventoSismico(
                fecha_hora_ocurrencia=datetime.strptime(fila['fecha_hora_ocurrencia'], '%Y-%m-%d %H:%M:%S'),
                latitud_epicentro=float(fila['latitud_epicentro']),
                longitud_epicentro=float(fila['longitud_epicentro']),
                latitud_hipocentro=float(fila['latitud_hipocentro']),
                longitud_hipocentro=float(fila['longitud_hipocentro']),
                valor_magnitud=float(fila['valor_magnitud']),
                cambio_estado=[]
            )
            evento.validar_y_asignar_clasificacion(fila['clasificacion_sismo'])
            evento.validar_y_asignar_origen(fila['origen_de_generacion'])
            evento.validar_y_asignar_alcance(fila['alcance_sismo'])

            estado_inicial = random.choice(estados_disponibles)
            if estado_inicial:
                cambio_estado_inicial = CambioEstado(
                    fecha_hora_inicio=datetime.now(),
                    estado=estado_inicial,
                    empleado=None
                )
                evento.cambio_estado.append(cambio_estado_inicial)
                evento.estado_actual = cambio_estado_inicial

            # Agregar series temporales mock, cada una con su propia estación y sismógrafo
            for i in range(1, random.randint(2, 4)):
                # Crear una estación sismológica para la serie temporal
                estacion = EstacionSismologica(
                    codigo_estacion=f"EST-{random.randint(100,999)}",
                    documento_certificacion_adq=f"DOC-{random.randint(1000,9999)}",
                    fecha_solicitud_certificacion=datetime.now().date(),
                    latitud=evento.latitud_epicentro,
                    longitud=evento.longitud_epicentro,
                    nombre=f"Estacion-{random.randint(1,10)}",
                    nro_certificacion_adquisicion=f"CERT-{random.randint(1000,9999)}"
                )
                # Crear un sismógrafo asociado a la estación
                sismografo = Sismografo(
                    fecha_adquisicion=datetime.now().date(),
                    identificador_sismografo=f"SIS-{random.randint(1000,9999)}",
                    nro_serie=f"SN-{random.randint(10000,99999)}"
                )
                sismografo.estacion_sismologica = estacion

                serie = SerieTemporal(
                    condicion_alarma=f"Alarma {i}",
                    fecha_hora_inicio_registro_muestras=evento.fecha_hora_ocurrencia,
                    fecha_hora_registro=evento.fecha_hora_ocurrencia + timedelta(minutes=i*5),
                    frecuencia_muestreo=100 + i*10
                )
                # Asociar sismógrafo a la serie temporal
                serie.set_sismografo(sismografo)
                sismografo.series_temporales.append(serie)
                # Agregar muestras sísmicas mock (1..*)
                for j in range(1, random.randint(2, 4)):
                    muestra = MuestraSismica(
                        fecha_hora_muestra=evento.fecha_hora_ocurrencia + timedelta(minutes=i*5 + j)
                    )
                    # Cada muestra tiene exactamente 3 detalles: velocidad, frecuencia y longitud
                    for idx in range(3):
                        valor = round(random.uniform(0.1, 10.0), 2)
                        detalle = DetalleMuestraSismica(valor=valor)
                        tipo_dato = TipoDeDato(
                            denominacion=denominaciones[idx],
                            nombre_unidad_medida=unidades[idx],
                            valor_umbral=round(random.uniform(1.0, 5.0), 2)
                        )
                        detalle.set_tipo_de_dato(tipo_dato)
                        muestra.agregar_detalle_muestra(detalle)
                    serie.agregar_muestra_sismica(muestra)
                evento.agregar_serie_temporal(serie)

            eventos.append(evento)
    return eventos

# Create a specific employee
empleado_prueba = Empleado(
    apellido="Perez",
    mail="perez@example.com",
    nombre="Juan",
    telefono="123456789",
    rol="Analista"
)

# Create a specific user and associate it with the employee
usuario_prueba = Usuario(nombre="jperez", contraseña="1234", empleado=empleado_prueba)
usuario_prueba.set_empleado(empleado_prueba)

# Create a session and associate it with the user
sesion_prueba = Sesion(fecha_hora_inicio=datetime.now(), fecha_hora_fin=None, usuario=usuario_prueba)

if __name__ == "__main__":
    # Cargar eventos desde el archivo CSV
    ruta_csv = "c:\\Users\\Martin Ferreyra\\OneDrive\\Desktop\\SISTEMAS\\TERCER AÑO\\DSI\\PRÁCTICO\\PPAI\\registrarResultadoDeRevisionManual\\eventos_sismicos.csv"
    eventos_cargados = cargar_eventos_desde_csv(ruta_csv)

    gestor = GestorSismo(sesion_prueba)

    # Agregar eventos cargados al gestor
    for evento in eventos_cargados:
        gestor.agregarEvento(evento)

    pantalla = PantallaAdmSismo(gestor) 
    
    # Mostrar menú principal antes de habilitar ventana
    opcion = mostrar_menu_opciones()
    if opcion == "Registrar resultado de revisión manual":
        pantalla.opc_res_rev_manual()
    else:
        print("Saliendo del sistema.")
        exit()
