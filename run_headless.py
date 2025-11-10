"""Runner ligero para comprobar que los datos y la lógica cargan sin iniciar la GUI.

Uso: python run_headless.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaz import main as interfaz_main


def main():
    ruta_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eventos_sismicos.csv')
    print(f"Cargando eventos desde: {ruta_csv}")
    eventos = interfaz_main.cargar_eventos_desde_csv(ruta_csv)
    print(f"Eventos cargados: {len(eventos)}")
    if eventos:
        e0 = eventos[0]
        print("Primer evento resumen:")
        try:
            print(f"  Fecha: {e0.fecha_hora_ocurrencia}")
            print(f"  Epicentro: {e0.latitud_epicentro}, {e0.longitud_epicentro}")
            print(f"  Magnitud: {e0.valor_magnitud}")
            print(f"  Series temporales: {len(getattr(e0, 'series_temporales', []))}")
        except Exception as ex:
            print("  Error al mostrar detalles del evento:", ex)


if __name__ == '__main__':
    main()
