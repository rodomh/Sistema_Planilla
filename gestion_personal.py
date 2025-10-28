"""
Módulo de Gestión de Personal y Ausencias
Funciones para registrar y gestionar ausencias, permisos y faltas
"""

from datetime import datetime, date, timedelta
from models import Empleado, Ausencia, Empresa
from decimal import Decimal

def registrar_ausencia(empleado_id, fecha, tipo, justificada=False, motivo='', horas_perdidas=8.0):
    """
    Registra una ausencia para un empleado
    
    Args:
        empleado_id: ID del empleado
        fecha: Fecha de la ausencia
        tipo: Tipo de ausencia ('falta', 'permiso', 'vacaciones', 'licencia')
        justificada: Si la ausencia está justificada
        motivo: Motivo de la ausencia
        horas_perdidas: Horas de trabajo perdidas (default 8.0)
    """
    from app import db
    ausencia = Ausencia(
        empleado_id=empleado_id,
        fecha=fecha,
        tipo=tipo,
        justificada=justificada,
        motivo=motivo,
        horas_perdidas=Decimal(str(horas_perdidas))
    )
    
    db.session.add(ausencia)
    db.session.commit()
    
    return ausencia

def obtener_ausencias_empleado(empleado_id, mes=None, año=None):
    """
    Obtiene las ausencias de un empleado en un período específico
    """
    from app import db
    query = Ausencia.query.filter_by(empleado_id=empleado_id)
    
    if mes and año:
        query = query.filter(
            db.extract('month', Ausencia.fecha) == mes,
            db.extract('year', Ausencia.fecha) == año
        )
    
    return query.order_by(Ausencia.fecha.desc()).all()

def obtener_ausencias_empresa(empresa_id, mes=None, año=None):
    """
    Obtiene todas las ausencias de una empresa en un período específico
    """
    query = db.session.query(Ausencia).join(Empleado).filter(Empleado.empresa_id == empresa_id)
    
    if mes and año:
        query = query.filter(
            db.extract('month', Ausencia.fecha) == mes,
            db.extract('year', Ausencia.fecha) == año
        )
    
    return query.order_by(Ausencia.fecha.desc()).all()

def calcular_dias_trabajados_mes(empleado_id, mes, año):
    """
    Calcula los días trabajados de un empleado en un mes específico
    """
    ausencias = obtener_ausencias_empleado(empleado_id, mes, año)
    
    # Contar faltas no justificadas
    faltas_no_justificadas = sum(1 for ausencia in ausencias 
                                if ausencia.tipo == 'falta' and not ausencia.justificada)
    
    # Días del mes (asumiendo 30 días laborales)
    dias_mes = 30
    dias_trabajados = dias_mes - faltas_no_justificadas
    
    return max(0, dias_trabajados), faltas_no_justificadas

def obtener_resumen_ausencias_empresa(empresa_id, mes, año):
    """
    Obtiene un resumen de ausencias por empresa
    """
    ausencias = obtener_ausencias_empresa(empresa_id, mes, año)
    
    resumen = {
        'total_ausencias': len(ausencias),
        'por_tipo': {},
        'por_empleado': {},
        'faltas_no_justificadas': 0,
        'permisos': 0,
        'vacaciones': 0,
        'licencias': 0
    }
    
    for ausencia in ausencias:
        tipo = ausencia.tipo
        empleado_nombre = f"{ausencia.empleado.nombres} {ausencia.empleado.apellidos}"
        
        # Contar por tipo
        resumen['por_tipo'][tipo] = resumen['por_tipo'].get(tipo, 0) + 1
        
        # Contar por empleado
        if empleado_nombre not in resumen['por_empleado']:
            resumen['por_empleado'][empleado_nombre] = 0
        resumen['por_empleado'][empleado_nombre] += 1
        
        # Contadores específicos
        if tipo == 'falta' and not ausencia.justificada:
            resumen['faltas_no_justificadas'] += 1
        elif tipo == 'permiso':
            resumen['permisos'] += 1
        elif tipo == 'vacaciones':
            resumen['vacaciones'] += 1
        elif tipo == 'licencia':
            resumen['licencias'] += 1
    
    return resumen

def registrar_permiso(empleado_id, fecha, motivo, horas_perdidas=8.0):
    """
    Registra un permiso justificado para un empleado
    """
    return registrar_ausencia(
        empleado_id=empleado_id,
        fecha=fecha,
        tipo='permiso',
        justificada=True,
        motivo=motivo,
        horas_perdidas=horas_perdidas
    )

def registrar_falta(empleado_id, fecha, motivo='', justificada=False):
    """
    Registra una falta para un empleado
    """
    return registrar_ausencia(
        empleado_id=empleado_id,
        fecha=fecha,
        tipo='falta',
        justificada=justificada,
        motivo=motivo,
        horas_perdidas=8.0
    )

def registrar_vacaciones(empleado_id, fecha_inicio, fecha_fin, motivo='Vacaciones'):
    """
    Registra un período de vacaciones para un empleado
    """
    # Calcular días de vacaciones
    fecha_actual = fecha_inicio
    dias_vacaciones = 0
    
    while fecha_actual <= fecha_fin:
        # Solo contar días laborales (lunes a viernes)
        if fecha_actual.weekday() < 5:  # 0-4 = lunes a viernes
            dias_vacaciones += 1
        fecha_actual += timedelta(days=1)
    
    # Registrar cada día de vacaciones
    ausencias = []
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() < 5:  # Solo días laborales
            ausencia = registrar_ausencia(
                empleado_id=empleado_id,
                fecha=fecha_actual,
                tipo='vacaciones',
                justificada=True,
                motivo=motivo,
                horas_perdidas=8.0
            )
            ausencias.append(ausencia)
        fecha_actual += timedelta(days=1)
    
    return ausencias

def justificar_ausencia(ausencia_id, motivo):
    """
    Justifica una ausencia existente
    """
    ausencia = Ausencia.query.get_or_404(ausencia_id)
    ausencia.justificada = True
    ausencia.motivo = motivo
    
    db.session.commit()
    
    return ausencia

def eliminar_ausencia(ausencia_id):
    """
    Elimina una ausencia del sistema
    """
    ausencia = Ausencia.query.get_or_404(ausencia_id)
    db.session.delete(ausencia)
    db.session.commit()
    
    return True

def obtener_estadisticas_ausencias(empresa_id, año=None):
    """
    Obtiene estadísticas de ausencias para una empresa
    """
    if not año:
        año = datetime.now().year
    
    ausencias = db.session.query(Ausencia).join(Empleado).filter(
        Empleado.empresa_id == empresa_id,
        db.extract('year', Ausencia.fecha) == año
    ).all()
    
    estadisticas = {
        'año': año,
        'total_ausencias': len(ausencias),
        'por_mes': {},
        'por_tipo': {},
        'por_empleado': {},
        'faltas_no_justificadas': 0,
        'promedio_mensual': 0
    }
    
    # Inicializar contadores por mes
    for mes in range(1, 13):
        estadisticas['por_mes'][mes] = 0
    
    for ausencia in ausencias:
        mes = ausencia.fecha.month
        tipo = ausencia.tipo
        empleado_nombre = f"{ausencia.empleado.nombres} {ausencia.empleado.apellidos}"
        
        # Contar por mes
        estadisticas['por_mes'][mes] += 1
        
        # Contar por tipo
        estadisticas['por_tipo'][tipo] = estadisticas['por_tipo'].get(tipo, 0) + 1
        
        # Contar por empleado
        estadisticas['por_empleado'][empleado_nombre] = estadisticas['por_empleado'].get(empleado_nombre, 0) + 1
        
        # Contar faltas no justificadas
        if tipo == 'falta' and not ausencia.justificada:
            estadisticas['faltas_no_justificadas'] += 1
    
    # Calcular promedio mensual
    meses_con_ausencias = sum(1 for count in estadisticas['por_mes'].values() if count > 0)
    if meses_con_ausencias > 0:
        estadisticas['promedio_mensual'] = estadisticas['total_ausencias'] / meses_con_ausencias
    
    return estadisticas

