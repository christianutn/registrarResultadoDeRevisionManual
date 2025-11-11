"""
Script para verificar los datos en la base de datos MySQL.
Muestra todos los eventos y sus estados actuales.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.db import get_session
from models.evento_sismico_model import EventoSismico
from models.cambio_estado_model import CambioEstado
from models.estado_model import Estado

def verificar_estados():
    """Verifica los estados de los eventos en la base de datos"""
    session = get_session()
    
    # Consultar todos los eventos
    eventos = session.query(EventoSismico).all()
    print(f"\n{'='*80}")
    print(f"📊 VERIFICACIÓN DE BASE DE DATOS")
    print(f"{'='*80}\n")
    print(f"Total de eventos en BD: {len(eventos)}\n")
    
    eventos_por_estado = {}
    
    for evento in eventos:
        print(f"{'─'*80}")
        print(f"🔹 Evento ID: {evento.id}")
        print(f"   Fecha: {evento.fecha_hora_ocurrencia}")
        print(f"   Magnitud: {evento.valor_magnitud}")
        print(f"   Epicentro: ({evento.latitud_epicentro}, {evento.longitud_epicentro})")
        
        # Buscar cambios de estado para este evento
        cambios = session.query(CambioEstado).filter_by(
            evento_sismico_id=evento.id
        ).order_by(CambioEstado.fecha_hora_inicio).all()
        
        print(f"\n   📋 Cambios de estado: {len(cambios)}")
        
        estado_actual = None
        for i, cambio in enumerate(cambios, 1):
            estado = session.query(Estado).filter_by(id=cambio.estado_id).first()
            if estado:
                fin = cambio.fecha_hora_fin if cambio.fecha_hora_fin else "⭐ ACTUAL"
                print(f"      {i}. {estado.nombre_estado.upper()} ({estado.ambito})")
                print(f"         Desde: {cambio.fecha_hora_inicio}")
                print(f"         Hasta: {fin}")
                
                # Si no tiene fecha_fin, es el estado actual
                if cambio.fecha_hora_fin is None:
                    estado_actual = estado.nombre_estado
        
        if estado_actual:
            print(f"\n   ✅ Estado actual: {estado_actual.upper()}")
            # Contar eventos por estado
            if estado_actual not in eventos_por_estado:
                eventos_por_estado[estado_actual] = 0
            eventos_por_estado[estado_actual] += 1
        else:
            print(f"\n   ⚠️ Sin estado actual definido")
        
        print()
    
    # Resumen
    print(f"{'='*80}")
    print(f"📊 RESUMEN POR ESTADO")
    print(f"{'='*80}\n")
    
    for estado, cantidad in eventos_por_estado.items():
        emoji = "✅" if estado in ["pendiente_revision", "auto_detectado"] else "📍"
        print(f"{emoji} {estado.upper()}: {cantidad} evento(s)")
    
    print(f"\n{'='*80}")
    print(f"Estados que se muestran en 'Registrar Revisión Manual':")
    print(f"  ✅ pendiente_revision")
    print(f"  ✅ auto_detectado")
    print(f"{'='*80}\n")
    
    # Verificar estados válidos
    estados_validos = ["pendiente_revision", "auto_detectado"]
    eventos_para_revisar = sum(
        cantidad for estado, cantidad in eventos_por_estado.items() 
        if estado in estados_validos
    )
    
    if eventos_para_revisar > 0:
        print(f"✅ Hay {eventos_para_revisar} evento(s) pendiente(s) de revisión\n")
    else:
        print(f"⚠️ NO hay eventos en estado 'pendiente_revision' o 'auto_detectado'")
        print(f"   La aplicación mostrará: 'No hay eventos pendientes de revisión'\n")
        print(f"💡 Para crear eventos revisables, ejecuta:")
        print(f"   UPDATE cambio_estado SET fecha_hora_fin = NULL")
        print(f"   WHERE estado_id IN (SELECT id FROM estado WHERE nombre_estado IN ('pendiente_revision', 'auto_detectado'))\n")
    
    session.close()

if __name__ == "__main__":
    try:
        verificar_estados()
    except Exception as e:
        print(f"\n❌ Error conectando a la base de datos:")
        print(f"   {str(e)}\n")
        print(f"Verifica:")
        print(f"  1. MySQL está corriendo")
        print(f"  2. Credenciales en config/db.py son correctas")
        print(f"  3. La base de datos 'bd_dsi' existe\n")
