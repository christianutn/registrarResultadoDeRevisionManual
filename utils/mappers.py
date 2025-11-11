"""
Mappers para convertir entre modelos SQLAlchemy y entidades del dominio.
Estos mappers permiten separar la capa de persistencia de la lógica de negocio.
"""

from modelo.Evento_Sismico import EventoSismico
from modelo.Cambio_Estado import CambioEstado
from modelo.Estado import Estado
from modelo.Empleado import Empleado
from modelo.Usuario import Usuario
from modelo.Alcance_Sismo import AlcanceSismo as AlcanceSismoEntidad
from modelo.Origen_De_Generacion import OrigenDeGeneracion as OrigenEntidad
from modelo.Clasificacion_Sismo import ClasificacionSismo as ClasificacionEntidad
from modelo.Serie_Temporal import SerieTemporal
from modelo.Sismografo import Sismografo
from modelo.Estacion_Sismologica import EstacionSismologica
from modelo.Muestra_Sismica import MuestraSismica
from modelo.Detalle_Muestra_Sismica import DetalleMuestraSismica
from modelo.Tipo_De_Dato import TipoDeDato


def evento_model_to_entity(evento_model):
    """
    Convierte un EventoSismicoModel (SQLAlchemy) a EventoSismico (entidad de dominio).
    Lee desde la base de datos SIN modificar nada.
    
    Args:
        evento_model: Instancia de models.evento_sismico_model.EventoSismico de la BD
        
    Returns:
        modelo.Evento_Sismico.EventoSismico: Entidad del dominio
    """
    from config.db import get_session
    from models.cambio_estado_model import CambioEstado as CambioEstadoModel
    from models.estado_model import Estado as EstadoModel
    from models.alcance_sismo_model import AlcanceSismo
    from models.origen_de_generacion_model import OrigenDeGeneracion
    from models.clasificacion_sismo_model import ClasificacionSismo
    
    evento = EventoSismico(
        fecha_hora_ocurrencia=evento_model.fecha_hora_ocurrencia,
        latitud_epicentro=evento_model.latitud_epicentro,
        longitud_epicentro=evento_model.longitud_epicentro,
        latitud_hipocentro=evento_model.latitud_hipocentro,
        longitud_hipocentro=evento_model.longitud_hipocentro,
        valor_magnitud=evento_model.valor_magnitud,
        cambio_estado=[]
    )
    
    # Guardar el ID de la BD para poder persistir cambios después
    evento.id_bd = evento_model.id
    
    # Obtener sesión para cargar relaciones
    session = get_session()
    
    # Asignar alcance, origen y clasificación desde la BD
    try:
        alcance = session.query(AlcanceSismo).filter_by(id=evento_model.alcance_sismo_id).first()
        if alcance:
            # Crear entidad directamente desde BD en lugar de buscar en mock
            evento.alcance_sismo = AlcanceSismoEntidad(alcance.nombre, alcance.descripcion)
    except Exception as e:
        print(f"Error cargando alcance: {e}")
    
    try:
        origen = session.query(OrigenDeGeneracion).filter_by(id=evento_model.origen_generacion_id).first()
        if origen:
            # Crear entidad directamente desde BD en lugar de buscar en mock
            evento.origen_de_generacion = OrigenEntidad(origen.descripcion, origen.nombre)
    except Exception as e:
        print(f"Error cargando origen: {e}")
    
    try:
        clasificacion = session.query(ClasificacionSismo).filter_by(id=evento_model.clasificacion_sismo_id).first()
        if clasificacion:
            # Crear entidad directamente desde BD en lugar de buscar en mock
            evento.clasificacion_sismo = ClasificacionEntidad(
                clasificacion.km_profundidad_desde,
                clasificacion.km_profundidad_hasta,
                clasificacion.nombre
            )
    except Exception as e:
        print(f"Error cargando clasificación: {e}")
    
    # Convertir cambios de estado desde la BD
    try:
        cambios_estado_db = session.query(CambioEstadoModel).filter_by(
            evento_sismico_id=evento_model.id
        ).order_by(CambioEstadoModel.fecha_hora_inicio).all()
        
        estado_actual_encontrado = False
        
        for cambio_model in cambios_estado_db:
            # Obtener el estado relacionado
            estado_model = session.query(EstadoModel).filter_by(id=cambio_model.estado_id).first()
            if estado_model:
                cambio = cambio_estado_model_to_entity(cambio_model, estado_model, session)
                evento.cambio_estado.append(cambio)
                
                # Si no tiene fecha_fin, es el estado actual
                if cambio_model.fecha_hora_fin is None and not estado_actual_encontrado:
                    evento.estado_actual = cambio.estado
                    estado_actual_encontrado = True
        
        # Si no se encontró ningún estado actual, usar el último cambio
        if not estado_actual_encontrado and len(evento.cambio_estado) > 0:
            ultimo_cambio = evento.cambio_estado[-1]
            evento.estado_actual = ultimo_cambio.estado
    except Exception as e:
        print(f"Error cargando cambios de estado: {e}")
    
    # Cargar series temporales desde la BD
    try:
        from models.serie_temporal_model import SerieTemporal as SerieTemporalModel
        
        series_temporales_db = session.query(SerieTemporalModel).filter_by(
            evento_sismico_id=evento_model.id
        ).all()
        
        for serie_model in series_temporales_db:
            serie = serie_temporal_model_to_entity(serie_model, session)
            evento.agregar_serie_temporal(serie)
    except Exception as e:
        print(f"Error cargando series temporales: {e}")
    
    session.close()
    return evento


def cambio_estado_model_to_entity(cambio_model, estado_model, session):
    """
    Convierte un CambioEstadoModel a CambioEstado (entidad).
    """
    from models.empleado_model import Empleado as EmpleadoModel
    
    # Convertir estado (solo nombre_estado y ambito, sin descripcion)
    estado = Estado(
        nombre_estado=estado_model.nombre_estado,
        ambito=estado_model.ambito
    )
    
    # Convertir empleado si existe
    empleado = None
    if cambio_model.empleado_id:
        try:
            empleado_model = session.query(EmpleadoModel).filter_by(id=cambio_model.empleado_id).first()
            if empleado_model:
                empleado = empleado_model_to_entity(empleado_model, session)
        except Exception as e:
            print(f"Error cargando empleado: {e}")
    
    cambio = CambioEstado(
        fecha_hora_inicio=cambio_model.fecha_hora_inicio,
        estado=estado,
        empleado=empleado
    )
    
    if cambio_model.fecha_hora_fin:
        cambio.set_fecha_hora_fin(cambio_model.fecha_hora_fin)
    
    return cambio


def empleado_model_to_entity(empleado_model, session):
    """
    Convierte un EmpleadoModel a Empleado (entidad).
    """
    from models.usuario_model import Usuario as UsuarioModel
    
    # El modelo de BD no tiene 'rol', usar valor por defecto
    empleado = Empleado(
        apellido=empleado_model.apellido,
        mail=empleado_model.mail if empleado_model.mail else "",
        nombre=empleado_model.nombre,
        telefono=empleado_model.telefono if empleado_model.telefono else "",
        rol="Analista"  # Rol por defecto - el modelo BD no tiene este campo
    )
    
    # Convertir usuario si existe
    try:
        usuario_model = session.query(UsuarioModel).filter_by(empleado_id=empleado_model.id).first()
        if usuario_model:
            usuario = usuario_model_to_entity(usuario_model)
            empleado.set_usuario(usuario)
    except Exception as e:
        print(f"Error cargando usuario: {e}")
    
    return empleado


def usuario_model_to_entity(usuario_model):
    """
    Convierte un UsuarioModel a Usuario (entidad).
    """
    return Usuario(
        nombre=usuario_model.nombre,
        contraseña=usuario_model.contraseña,
        empleado=None  # Se establecerá después
    )


def serie_temporal_model_to_entity(serie_model, session):
    """
    Convierte un SerieTemporalModel a SerieTemporal (entidad).
    Carga sismógrafo, estación y muestras sísmicas relacionadas.
    """
    from models.sismografo_model import Sismografo as SismografoModel
    from models.muestra_sismica_model import MuestraSismica as MuestraSismicaModel
    
    # Crear entidad serie temporal
    serie = SerieTemporal(
        condicion_alarma=serie_model.condicion_alarma,
        fecha_hora_inicio_registro_muestras=serie_model.fecha_hora_registro_muestras,
        fecha_hora_registro=serie_model.fecha_hora_registro,
        frecuencia_muestreo=serie_model.frecuencia_muestreo
    )
    
    # Cargar sismógrafo relacionado
    try:
        if serie_model.sismografo_id:
            sismografo_model = session.query(SismografoModel).filter_by(id=serie_model.sismografo_id).first()
            if sismografo_model:
                sismografo = sismografo_model_to_entity(sismografo_model, session)
                serie.set_sismografo(sismografo)
    except Exception as e:
        print(f"Error cargando sismógrafo: {e}")
    
    # Cargar muestras sísmicas relacionadas
    try:
        muestras_db = session.query(MuestraSismicaModel).filter_by(
            serie_temporal_id=serie_model.id
        ).all()
        
        for muestra_model in muestras_db:
            muestra = muestra_sismica_model_to_entity(muestra_model, session)
            serie.agregar_muestra_sismica(muestra)
    except Exception as e:
        print(f"Error cargando muestras sísmicas: {e}")
    
    return serie


def sismografo_model_to_entity(sismografo_model, session):
    """
    Convierte un SismografoModel a Sismografo (entidad).
    """
    from models.estacion_sismologica_model import EstacionSismologica as EstacionModel
    
    sismografo = Sismografo(
        fecha_adquisicion=sismografo_model.fecha_adquisicion,
        identificador_sismografo=sismografo_model.identificador_sismografo,
        nro_serie=sismografo_model.nro_serie
    )
    
    # Cargar estación sismológica
    try:
        if sismografo_model.estacion_sismologica_id:
            estacion_model = session.query(EstacionModel).filter_by(
                id=sismografo_model.estacion_sismologica_id
            ).first()
            if estacion_model:
                estacion = estacion_sismologica_model_to_entity(estacion_model)
                sismografo.estacion_sismologica = estacion
    except Exception as e:
        print(f"Error cargando estación sismológica: {e}")
    
    return sismografo


def estacion_sismologica_model_to_entity(estacion_model):
    """
    Convierte un EstacionSismologicaModel a EstacionSismologica (entidad).
    """
    return EstacionSismologica(
        codigo_estacion=estacion_model.codigo_estacion,
        documento_certificacion_adq=estacion_model.documento_certificacion_adq,
        fecha_solicitud_certificacion=estacion_model.fecha_solicitud_certificacion,
        latitud=estacion_model.latitud,
        longitud=estacion_model.longitud,
        nombre=estacion_model.nombre,
        nro_certificacion_adquisicion=estacion_model.nro_certificacion_adquisicion
    )


def muestra_sismica_model_to_entity(muestra_model, session):
    """
    Convierte un MuestraSismicaModel a MuestraSismica (entidad).
    """
    from models.detalle_muestra_sismica_model import DetalleMuestraSismica as DetalleModel
    
    muestra = MuestraSismica(
        fecha_hora_muestra=muestra_model.fecha_hora_muestra
    )
    
    # Cargar detalles de muestra
    try:
        detalles_db = session.query(DetalleModel).filter_by(
            muestra_sismica_id=muestra_model.id
        ).all()
        
        for detalle_model in detalles_db:
            detalle = detalle_muestra_sismica_model_to_entity(detalle_model, session)
            muestra.agregar_detalle_muestra(detalle)
    except Exception as e:
        print(f"Error cargando detalles de muestra: {e}")
    
    return muestra


def detalle_muestra_sismica_model_to_entity(detalle_model, session):
    """
    Convierte un DetalleMuestraSismicaModel a DetalleMuestraSismica (entidad).
    """
    from models.tipo_de_dato_model import TipoDeDato as TipoDeDatoModel
    
    detalle = DetalleMuestraSismica(
        valor=detalle_model.valor
    )
    
    # Cargar tipo de dato
    try:
        if detalle_model.tipo_de_dato_id:
            tipo_dato_model = session.query(TipoDeDatoModel).filter_by(
                id=detalle_model.tipo_de_dato_id
            ).first()
            if tipo_dato_model:
                tipo_dato = tipo_de_dato_model_to_entity(tipo_dato_model)
                detalle.set_tipo_de_dato(tipo_dato)
    except Exception as e:
        print(f"Error cargando tipo de dato: {e}")
    
    return detalle


def tipo_de_dato_model_to_entity(tipo_dato_model):
    """
    Convierte un TipoDeDatoModel a TipoDeDato (entidad).
    """
    return TipoDeDato(
        denominacion=tipo_dato_model.denominacion,
        nombre_unidad_medida=tipo_dato_model.nombre_unidad_medida,
        valor_umbral=tipo_dato_model.valor_umbral
    )


def guardar_cambio_estado_en_bd(evento_entidad, evento_id):
    """
    Guarda los cambios de estado de un evento en la base de datos.
    - Cierra el cambio de estado anterior (si existe)
    - Crea un nuevo cambio de estado con el estado actual
    
    Args:
        evento_entidad: Entidad EventoSismico con los cambios en memoria
        evento_id: ID del evento en la base de datos
    """
    from config.db import get_session
    from models.cambio_estado_model import CambioEstado as CambioEstadoModel
    from models.estado_model import Estado as EstadoModel
    from models.empleado_model import Empleado as EmpleadoModel
    
    session = get_session()
    
    try:
        # Obtener el último cambio de estado (el que se acaba de crear en memoria)
        if not evento_entidad.cambio_estado:
            print("⚠️  No hay cambios de estado para guardar")
            return False
        
        ultimo_cambio = evento_entidad.cambio_estado[-1]
        
        # 1. Cerrar el cambio de estado anterior (poner fecha_hora_fin)
        cambios_anteriores = session.query(CambioEstadoModel).filter_by(
            evento_sismico_id=evento_id,
            fecha_hora_fin=None
        ).all()
        
        for cambio_anterior in cambios_anteriores:
            cambio_anterior.fecha_hora_fin = ultimo_cambio.fecha_hora_inicio
            print(f"✅ Cerrado cambio de estado anterior (ID {cambio_anterior.id})")
        
        # 2. Buscar el ID del estado en la BD
        estado_model = session.query(EstadoModel).filter_by(
            nombre_estado=ultimo_cambio.estado.nombre_estado,
            ambito=ultimo_cambio.estado.ambito
        ).first()
        
        if not estado_model:
            print(f"❌ No se encontró el estado: {ultimo_cambio.estado.nombre_estado}")
            session.close()
            return False
        
        # 3. Buscar el ID del empleado en la BD
        empleado_id = None
        if ultimo_cambio.empleado:
            # Manejar tanto objetos Empleado como diccionarios
            if isinstance(ultimo_cambio.empleado, dict):
                apellido = ultimo_cambio.empleado.get('apellido', '')
                nombre = ultimo_cambio.empleado.get('nombre', '')
            else:
                apellido = getattr(ultimo_cambio.empleado, 'apellido', '')
                nombre = getattr(ultimo_cambio.empleado, 'nombre', '')
            
            empleado_model = session.query(EmpleadoModel).filter_by(
                apellido=apellido,
                nombre=nombre
            ).first()
            
            if empleado_model:
                empleado_id = empleado_model.id
            else:
                print(f"⚠️  No se encontró el empleado: {nombre} {apellido}")
                # Usar empleado por defecto
                empleado_id = 1
        else:
            # Si no hay empleado, usar el empleado por defecto
            empleado_id = 1
        
        # 4. Crear el nuevo cambio de estado en la BD
        nuevo_cambio_bd = CambioEstadoModel(
            fecha_hora_inicio=ultimo_cambio.fecha_hora_inicio,
            fecha_hora_fin=ultimo_cambio.fecha_hora_fin if hasattr(ultimo_cambio, 'fecha_hora_fin') else None,
            estado_id=estado_model.id,
            evento_sismico_id=evento_id,
            empleado_id=empleado_id
        )
        
        session.add(nuevo_cambio_bd)
        session.commit()
        
        print(f"✅ Cambio de estado guardado en BD: {ultimo_cambio.estado.nombre_estado}")
        print(f"   Evento ID: {evento_id}, Estado: {estado_model.nombre_estado}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error guardando cambio de estado: {e}")
        session.rollback()
        session.close()
        return False
