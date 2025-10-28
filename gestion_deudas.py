"""
Módulo de Gestión de Deudas Internas
Funciones para gestionar préstamos y adelantos de empleados
"""

from datetime import datetime, date, timedelta
from models import Empleado, Prestamo, Adelanto, Empresa
from decimal import Decimal
import math

def crear_prestamo(empleado_id, monto_total, cuotas, motivo='', fecha_prestamo=None):
    """
    Crea un nuevo préstamo para un empleado
    
    Args:
        empleado_id: ID del empleado
        monto_total: Monto total del préstamo
        cuotas: Número de cuotas mensuales
        motivo: Motivo del préstamo
        fecha_prestamo: Fecha del préstamo (default: hoy)
    """
    from app import db
    if not fecha_prestamo:
        fecha_prestamo = date.today()
    
    cuota_mensual = Decimal(str(monto_total)) / Decimal(str(cuotas))
    
    # Calcular fecha de finalización
    fecha_finalizacion = fecha_prestamo + timedelta(days=cuotas * 30)  # Aproximación
    
    prestamo = Prestamo(
        empleado_id=empleado_id,
        monto_total=Decimal(str(monto_total)),
        monto_pendiente=Decimal(str(monto_total)),
        cuota_mensual=cuota_mensual,
        fecha_prestamo=fecha_prestamo,
        fecha_finalizacion=fecha_finalizacion,
        motivo=motivo,
        activo=True
    )
    
    db.session.add(prestamo)
    db.session.commit()
    
    return prestamo

def crear_adelanto(empleado_id, monto, mes_aplicar, año_aplicar, motivo=''):
    """
    Crea un adelanto de sueldo para un empleado
    
    Args:
        empleado_id: ID del empleado
        monto: Monto del adelanto
        mes_aplicar: Mes en que se descuenta
        año_aplicar: Año en que se descuenta
        motivo: Motivo del adelanto
    """
    adelanto = Adelanto(
        empleado_id=empleado_id,
        monto=Decimal(str(monto)),
        fecha_adelanto=date.today(),
        mes_aplicar=mes_aplicar,
        año_aplicar=año_aplicar,
        motivo=motivo,
        aplicado=False
    )
    
    db.session.add(adelanto)
    db.session.commit()
    
    return adelanto

def obtener_prestamos_empleado(empleado_id, activos_only=True):
    """
    Obtiene los préstamos de un empleado
    """
    query = Prestamo.query.filter_by(empleado_id=empleado_id)
    
    if activos_only:
        query = query.filter_by(activo=True)
    
    return query.order_by(Prestamo.fecha_prestamo.desc()).all()

def obtener_adelantos_empleado(empleado_id, aplicados_only=False):
    """
    Obtiene los adelantos de un empleado
    """
    query = Adelanto.query.filter_by(empleado_id=empleado_id)
    
    if aplicados_only:
        query = query.filter_by(aplicado=True)
    else:
        query = query.filter_by(aplicado=False)
    
    return query.order_by(Adelanto.fecha_adelanto.desc()).all()

def obtener_deudas_empresa(empresa_id):
    """
    Obtiene todas las deudas internas de una empresa
    """
    empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
    
    deudas = {
        'prestamos': [],
        'adelantos': [],
        'totales': {
            'prestamos_pendientes': Decimal('0'),
            'adelantos_pendientes': Decimal('0'),
            'total_deudas': Decimal('0')
        }
    }
    
    for empleado in empleados:
        # Préstamos activos
        prestamos = obtener_prestamos_empleado(empleado.id, activos_only=True)
        for prestamo in prestamos:
            deudas['prestamos'].append({
                'id': prestamo.id,
                'empleado': f"{empleado.nombres} {empleado.apellidos}",
                'monto_total': float(prestamo.monto_total),
                'monto_pendiente': float(prestamo.monto_pendiente),
                'cuota_mensual': float(prestamo.cuota_mensual),
                'fecha_prestamo': prestamo.fecha_prestamo,
                'motivo': prestamo.motivo
            })
            deudas['totales']['prestamos_pendientes'] += prestamo.monto_pendiente
        
        # Adelantos pendientes
        adelantos = obtener_adelantos_empleado(empleado.id, aplicados_only=False)
        for adelanto in adelantos:
            deudas['adelantos'].append({
                'id': adelanto.id,
                'empleado': f"{empleado.nombres} {empleado.apellidos}",
                'monto': float(adelanto.monto),
                'mes_aplicar': adelanto.mes_aplicar,
                'año_aplicar': adelanto.año_aplicar,
                'fecha_adelanto': adelanto.fecha_adelanto,
                'motivo': adelanto.motivo
            })
            deudas['totales']['adelantos_pendientes'] += adelanto.monto
    
    deudas['totales']['total_deudas'] = (
        deudas['totales']['prestamos_pendientes'] + 
        deudas['totales']['adelantos_pendientes']
    )
    
    # Convertir Decimal a float para JSON
    deudas['totales']['prestamos_pendientes'] = float(deudas['totales']['prestamos_pendientes'])
    deudas['totales']['adelantos_pendientes'] = float(deudas['totales']['adelantos_pendientes'])
    deudas['totales']['total_deudas'] = float(deudas['totales']['total_deudas'])
    
    return deudas

def procesar_pago_prestamo(prestamo_id, monto_pago):
    """
    Procesa un pago de préstamo
    """
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    
    monto_pago_decimal = Decimal(str(monto_pago))
    
    if monto_pago_decimal >= prestamo.monto_pendiente:
        # Pago completo
        prestamo.monto_pendiente = Decimal('0')
        prestamo.activo = False
        prestamo.fecha_finalizacion = date.today()
    else:
        # Pago parcial
        prestamo.monto_pendiente -= monto_pago_decimal
    
    db.session.commit()
    
    return prestamo

def calcular_cuota_prestamo(monto_total, cuotas, tasa_interes=0):
    """
    Calcula la cuota mensual de un préstamo
    
    Args:
        monto_total: Monto total del préstamo
        cuotas: Número de cuotas
        tasa_interes: Tasa de interés mensual (default: 0 - sin interés)
    """
    monto = Decimal(str(monto_total))
    num_cuotas = Decimal(str(cuotas))
    tasa = Decimal(str(tasa_interes))
    
    if tasa == 0:
        # Sin interés
        cuota_mensual = monto / num_cuotas
    else:
        # Con interés (fórmula de cuota fija)
        tasa_mensual = tasa / Decimal('100')
        cuota_mensual = monto * (tasa_mensual * (1 + tasa_mensual) ** num_cuotas) / ((1 + tasa_mensual) ** num_cuotas - 1)
    
    return cuota_mensual

def obtener_resumen_deudas_empleado(empleado_id):
    """
    Obtiene un resumen de deudas de un empleado
    """
    prestamos = obtener_prestamos_empleado(empleado_id, activos_only=True)
    adelantos = obtener_adelantos_empleado(empleado_id, aplicados_only=False)
    
    resumen = {
        'prestamos_activos': len(prestamos),
        'adelantos_pendientes': len(adelantos),
        'total_prestamos_pendiente': sum(p.monto_pendiente for p in prestamos),
        'total_adelantos_pendiente': sum(a.monto for a in adelantos),
        'cuota_mensual_total': sum(p.cuota_mensual for p in prestamos),
        'adelantos_mes_actual': 0
    }
    
    # Calcular adelantos del mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    adelantos_mes = [a for a in adelantos if a.mes_aplicar == mes_actual and a.año_aplicar == año_actual]
    resumen['adelantos_mes_actual'] = sum(a.monto for a in adelantos_mes)
    
    # Convertir Decimal a float
    resumen['total_prestamos_pendiente'] = float(resumen['total_prestamos_pendiente'])
    resumen['total_adelantos_pendiente'] = float(resumen['total_adelantos_pendiente'])
    resumen['cuota_mensual_total'] = float(resumen['cuota_mensual_total'])
    resumen['adelantos_mes_actual'] = float(resumen['adelantos_mes_actual'])
    
    return resumen

def cancelar_prestamo(prestamo_id):
    """
    Cancela un préstamo (marca como inactivo)
    """
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    prestamo.activo = False
    prestamo.fecha_finalizacion = date.today()
    
    db.session.commit()
    
    return prestamo

def cancelar_adelanto(adelanto_id):
    """
    Cancela un adelanto (lo marca como aplicado sin descuento)
    """
    adelanto = Adelanto.query.get_or_404(adelanto_id)
    adelanto.aplicado = True
    
    db.session.commit()
    
    return adelanto

def obtener_historial_pagos_empleado(empleado_id):
    """
    Obtiene el historial de pagos de préstamos de un empleado
    """
    # Esta función requeriría una tabla adicional de historial de pagos
    # Por ahora retornamos información básica de los préstamos
    prestamos = Prestamo.query.filter_by(empleado_id=empleado_id).all()
    
    historial = []
    for prestamo in prestamos:
        historial.append({
            'id': prestamo.id,
            'monto_total': float(prestamo.monto_total),
            'monto_pendiente': float(prestamo.monto_pendiente),
            'cuota_mensual': float(prestamo.cuota_mensual),
            'fecha_prestamo': prestamo.fecha_prestamo,
            'fecha_finalizacion': prestamo.fecha_finalizacion,
            'activo': prestamo.activo,
            'motivo': prestamo.motivo
        })
    
    return historial

def validar_capacidad_pago(empleado_id, monto_nuevo_prestamo):
    """
    Valida si un empleado tiene capacidad de pago para un nuevo préstamo
    """
    empleado = Empleado.query.get_or_404(empleado_id)
    resumen = obtener_resumen_deudas_empleado(empleado_id)
    
    sueldo_mensual = empleado.sueldo_base
    deudas_mensuales = resumen['cuota_mensual_total'] + resumen['adelantos_mes_actual']
    
    # Calcular cuota del nuevo préstamo (sin interés por simplicidad)
    cuota_nueva = Decimal(str(monto_nuevo_prestamo)) / Decimal('12')  # Asumiendo 12 cuotas
    
    # Regla: las deudas no deben exceder el 30% del sueldo
    limite_deudas = sueldo_mensual * Decimal('0.30')
    deudas_totales = deudas_mensuales + cuota_nueva
    
    capacidad = {
        'puede_solicitar': deudas_totales <= limite_deudas,
        'sueldo_mensual': float(sueldo_mensual),
        'deudas_actuales': float(deudas_mensuales),
        'cuota_nueva': float(cuota_nueva),
        'deudas_totales': float(deudas_totales),
        'limite_recomendado': float(limite_deudas),
        'porcentaje_utilizado': float((deudas_totales / sueldo_mensual) * 100)
    }
    
    return capacidad

