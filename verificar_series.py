"""Script para verificar series temporales en la BD"""
from config.db import get_session
from models.serie_temporal_model import SerieTemporal
from models.muestra_sismica_model import MuestraSismica
from models.detalle_muestra_sismica_model import DetalleMuestraSismica

session = get_session()

# Verificar series del evento 1
series = session.query(SerieTemporal).filter_by(evento_sismico_id=1).all()

print(f"\n📊 Series temporales para evento 1: {len(series)}")
for s in series:
    print(f"\n  Serie ID: {s.id}")
    print(f"    Condición: {s.condicion_alarma}")
    print(f"    Frecuencia: {s.frecuencia_muestreo} Hz")
    print(f"    Sismografo ID: {s.sismografo_id}")
    
    # Verificar muestras de esta serie
    muestras = session.query(MuestraSismica).filter_by(serie_temporal_id=s.id).all()
    print(f"    Muestras: {len(muestras)}")
    
    for m in muestras:
        print(f"      - Muestra ID {m.id}: {m.fecha_hora_muestra}")
        
        # Verificar detalles de cada muestra
        detalles = session.query(DetalleMuestraSismica).filter_by(muestra_sismica_id=m.id).all()
        print(f"        Detalles: {len(detalles)}")
        for d in detalles:
            print(f"          * Valor: {d.valor}, Tipo dato ID: {d.tipo_de_dato_id}")

session.close()
