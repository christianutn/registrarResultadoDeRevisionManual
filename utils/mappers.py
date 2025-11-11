"""
Mappers para convertir entre modelos SQLAlchemy y entidades del dominio.
Estos mappers permiten separar la capa de persistencia de la lógica de negocio.
"""

from modelo.Evento_Sismico import EventoSismico
from modelo.Cambio_Estado import CambioEstado
from modelo.Estado import Estado
from modelo.Empleado import Empleado
from modelo.Usuario import Usuario


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
    
    # Obtener sesión para cargar relaciones
    session = get_session()
    
    # Asignar alcance, origen y clasificación desde la BD
    try:
        alcance = session.query(AlcanceSismo).filter_by(id=evento_model.alcance_sismo_id).first()
        if alcance:
            evento.validar_y_asignar_alcance(alcance.nombre)
    except Exception as e:
        print(f"Error cargando alcance: {e}")
    
    try:
        origen = session.query(OrigenDeGeneracion).filter_by(id=evento_model.origen_generacion_id).first()
        if origen:
            evento.validar_y_asignar_origen(origen.nombre)
    except Exception as e:
        print(f"Error cargando origen: {e}")
    
    try:
        clasificacion = session.query(ClasificacionSismo).filter_by(id=evento_model.clasificacion_sismo_id).first()
        if clasificacion:
            evento.validar_y_asignar_clasificacion(clasificacion.nombre)
    except Exception as e:
        print(f"Error cargando clasificación: {e}")
    
    # Convertir cambios de estado desde la BD
    try:
        cambios_estado_db = session.query(CambioEstadoModel).filter_by(
            evento_sismico_id=evento_model.id
        ).all()
        
        for cambio_model in cambios_estado_db:
            # Obtener el estado relacionado
            estado_model = session.query(EstadoModel).filter_by(id=cambio_model.estado_id).first()
            if estado_model:
                cambio = cambio_estado_model_to_entity(cambio_model, estado_model, session)
                evento.cambio_estado.append(cambio)
                
                # Si no tiene fecha_fin, es el estado actual
                if cambio_model.fecha_hora_fin is None:
                    evento.estado_actual = cambio.estado
    except Exception as e:
        print(f"Error cargando cambios de estado: {e}")
    
    session.close()
    return evento


def cambio_estado_model_to_entity(cambio_model, estado_model, session):
    """
    Convierte un CambioEstadoModel a CambioEstado (entidad).
    """
    from models.empleado_model import Empleado as EmpleadoModel
    
    # Convertir estado
    estado = Estado(
        nombre_estado=estado_model.nombre_estado,
        descripcion="",  # No está en el modelo
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
    
    empleado = Empleado(
        apellido=empleado_model.apellido,
        mail=empleado_model.mail,
        nombre=empleado_model.nombre,
        telefono=empleado_model.telefono,
        rol=empleado_model.rol
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
