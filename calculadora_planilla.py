"""
Calculadora de Planilla Multirégimen para Perú
Implementa la lógica de cálculo de beneficios sociales y descuentos
según el régimen laboral de la empresa (Microempresa, Pequeña Empresa, General)
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from models import Empresa, Empleado, Locador, Ausencia, Prestamo, Adelanto, Pago, PagoLocador, Configuracion

# Constantes del sistema laboral peruano
ASIGNACION_FAMILIAR = Decimal('102.50')
UMBRAL_ASIGNACION_FAMILIAR = Decimal('1025.00')
UMBRAL_RETENCION_4TA_CAT = Decimal('1500.00')
TASA_RETENCION_4TA_CAT = Decimal('0.08')
TASA_PENSION_ONP = Decimal('0.13')

# Tasas de AFP (ejemplo - deben ser configurables)
TASAS_AFP = {
    'PRIMA': Decimal('0.12'),
    'INTEGRA': Decimal('0.12'),
    'PROFUTURO': Decimal('0.12'),
    'HABITAT': Decimal('0.12')
}

def obtener_configuracion(clave, valor_default='0'):
    """Obtiene configuración del sistema o retorna valor por defecto"""
    config = Configuracion.query.filter_by(clave=clave).first()
    return Decimal(config.valor) if config else Decimal(valor_default)

def calcular_dias_trabajados(empleado_id, mes, año):
    """Calcula los días trabajados de un empleado en un mes específico"""
    from app import db
    # Obtener ausencias del mes
    ausencias = Ausencia.query.filter(
        Ausencia.empleado_id == empleado_id,
        db.extract('month', Ausencia.fecha) == mes,
        db.extract('year', Ausencia.fecha) == año
    ).all()
    
    # Calcular días perdidos
    dias_perdidos = sum(1 for ausencia in ausencias if ausencia.tipo == 'falta')
    
    # Días del mes (asumiendo 30 días laborales)
    dias_mes = 30
    dias_trabajados = dias_mes - dias_perdidos
    
    return max(0, dias_trabajados), dias_perdidos

def calcular_beneficios_sociales(empleado, empresa, mes, año):
    """
    Calcula beneficios sociales según el régimen laboral de la empresa
    """
    regimen = empresa.regimen_laboral
    sueldo_base = empleado.sueldo_base
    
    beneficios = {
        'vacaciones': Decimal('0'),
        'cts': Decimal('0'),
        'gratificacion': Decimal('0'),
        'asignacion_familiar': Decimal('0')
    }
    
    # Vacaciones anuales
    if regimen in ['microempresa', 'pequeña_empresa']:
        beneficios['vacaciones'] = (sueldo_base * Decimal('15')) / Decimal('360')  # 15 días al año
    elif regimen == 'general':
        beneficios['vacaciones'] = (sueldo_base * Decimal('30')) / Decimal('360')  # 30 días al año
    
    # CTS (Compensación por Tiempo de Servicios)
    if regimen == 'pequeña_empresa':
        # Media remuneración anual (15 días por año de servicio)
        años_servicio = calcular_años_servicio(empleado.fecha_ingreso)
        beneficios['cts'] = (sueldo_base * Decimal('15') * años_servicio) / Decimal('12')
    elif regimen == 'general':
        # Un sueldo anual
        años_servicio = calcular_años_servicio(empleado.fecha_ingreso)
        beneficios['cts'] = (sueldo_base * Decimal('30') * años_servicio) / Decimal('12')
    # Microempresa: NO corresponde CTS
    
    # Gratificaciones (Julio y Diciembre)
    if mes in [7, 12]:  # Julio y Diciembre
        if regimen == 'pequeña_empresa':
            beneficios['gratificacion'] = sueldo_base / Decimal('2')  # Medio sueldo
        elif regimen == 'general':
            beneficios['gratificacion'] = sueldo_base + (sueldo_base * Decimal('0.09'))  # Sueldo + 9% bonificación
        # Microempresa: NO corresponde gratificaciones
    
    # Asignación Familiar
    if regimen in ['pequeña_empresa', 'general']:
        if sueldo_base <= UMBRAL_ASIGNACION_FAMILIAR:
            beneficios['asignacion_familiar'] = ASIGNACION_FAMILIAR
    # Microempresa: NO corresponde asignación familiar
    
    return beneficios

def calcular_años_servicio(fecha_ingreso):
    """Calcula los años de servicio de un empleado"""
    hoy = date.today()
    años = hoy.year - fecha_ingreso.year
    if hoy.month < fecha_ingreso.month or (hoy.month == fecha_ingreso.month and hoy.day < fecha_ingreso.day):
        años -= 1
    return max(0, años)

def calcular_descuentos_empleado(empleado, mes, año):
    """
    Calcula descuentos para empleados (pensión e impuesto a la renta)
    """
    sueldo_base = empleado.sueldo_base
    
    descuentos = {
        'pension': Decimal('0'),
        'impuesto_renta': Decimal('0')
    }
    
    # Cálculo de pensión
    if empleado.tipo_pension == 'ONP':
        descuentos['pension'] = sueldo_base * TASA_PENSION_ONP
    elif empleado.tipo_pension == 'AFP' and empleado.afp_codigo:
        tasa_afp = TASAS_AFP.get(empleado.afp_codigo, Decimal('0.12'))
        descuentos['pension'] = sueldo_base * tasa_afp
    
    # Impuesto a la Renta 5ta Categoría
    # Umbral mínimo no afecto (debe ser configurable)
    umbral_minimo = obtener_configuracion('umbral_renta_5ta', '1025')
    if sueldo_base > umbral_minimo:
        # Cálculo simplificado del impuesto a la renta
        base_imponible = sueldo_base - umbral_minimo
        if base_imponible <= Decimal('500'):
            descuentos['impuesto_renta'] = base_imponible * Decimal('0.08')
        elif base_imponible <= Decimal('1000'):
            descuentos['impuesto_renta'] = Decimal('40') + ((base_imponible - Decimal('500')) * Decimal('0.14'))
        else:
            descuentos['impuesto_renta'] = Decimal('110') + ((base_imponible - Decimal('1000')) * Decimal('0.17'))
    
    return descuentos

def calcular_deudas_internas(empleado_id, mes, año):
    """
    Calcula descuentos por préstamos y adelantos
    """
    descuentos = {
        'prestamos': Decimal('0'),
        'adelantos': Decimal('0')
    }
    
    # Préstamos activos
    prestamos = Prestamo.query.filter(
        Prestamo.empleado_id == empleado_id,
        Prestamo.activo == True
    ).all()
    
    for prestamo in prestamos:
        descuentos['prestamos'] += prestamo.cuota_mensual
    
    # Adelantos del mes
    adelantos = Adelanto.query.filter(
        Adelanto.empleado_id == empleado_id,
        Adelanto.mes_aplicar == mes,
        Adelanto.año_aplicar == año,
        Adelanto.aplicado == False
    ).all()
    
    for adelanto in adelantos:
        descuentos['adelantos'] += adelanto.monto
        adelanto.aplicado = True  # Marcar como aplicado
    
    return descuentos

def calcular_planilla_empleado(empleado, empresa, mes, año, tipo_pago='mensual'):
    """
    Calcula la planilla completa de un empleado
    """
    # Calcular días trabajados
    dias_trabajados, dias_faltados = calcular_dias_trabajados(empleado.id, mes, año)
    
    # Sueldo proporcional por días trabajados
    sueldo_proporcional = (empleado.sueldo_base * dias_trabajados) / Decimal('30')
    
    # Calcular beneficios sociales
    beneficios = calcular_beneficios_sociales(empleado, empresa, mes, año)
    
    # Calcular descuentos
    descuentos_empleado = calcular_descuentos_empleado(empleado, mes, año)
    deudas = calcular_deudas_internas(empleado.id, mes, año)
    
    # Totales
    total_ingresos = sueldo_proporcional + sum(beneficios.values())
    total_descuentos = sum(descuentos_empleado.values()) + sum(deudas.values())
    neto_pagar = total_ingresos - total_descuentos
    
    # Crear registro de pago
    pago = Pago(
        empleado_id=empleado.id,
        mes=mes,
        año=año,
        tipo_pago=tipo_pago,
        sueldo_base=sueldo_proporcional,
        dias_trabajados=dias_trabajados,
        dias_faltados=dias_faltados,
        vacaciones=beneficios['vacaciones'],
        cts=beneficios['cts'],
        gratificacion=beneficios['gratificacion'],
        asignacion_familiar=beneficios['asignacion_familiar'],
        pension=descuentos_empleado['pension'],
        impuesto_renta=descuentos_empleado['impuesto_renta'],
        prestamos=deudas['prestamos'],
        adelantos=deudas['adelantos'],
        total_ingresos=total_ingresos,
        total_descuentos=total_descuentos,
        neto_pagar=neto_pagar
    )
    
    return pago

def calcular_planilla_locador(locador, mes, año):
    """
    Calcula el pago para un locador de servicios
    """
    monto_bruto = locador.monto_mensual
    retencion_4ta_cat = Decimal('0')
    
    # Retención 4ta Categoría (8% si supera el umbral y no está suspendido)
    if not locador.suspendido and monto_bruto > UMBRAL_RETENCION_4TA_CAT:
        retencion_4ta_cat = monto_bruto * TASA_RETENCION_4TA_CAT
    
    neto_pagar = monto_bruto - retencion_4ta_cat
    
    # Crear registro de pago
    pago_locador = PagoLocador(
        locador_id=locador.id,
        mes=mes,
        año=año,
        monto_bruto=monto_bruto,
        retencion_4ta_cat=retencion_4ta_cat,
        neto_pagar=neto_pagar
    )
    
    return pago_locador

def calcular_planilla_completa(empresa_id, mes, año):
    """
    Función principal que calcula la planilla completa de una empresa
    """
    empresa = Empresa.query.get_or_404(empresa_id)
    
    # Obtener empleados y locadores activos
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    resultados = {
        'empresa': empresa.nombre,
        'regimen_laboral': empresa.regimen_laboral,
        'mes': mes,
        'año': año,
        'empleados': [],
        'locadores': [],
        'totales': {
            'total_empleados': 0,
            'total_locadores': 0,
            'total_ingresos': Decimal('0'),
            'total_descuentos': Decimal('0'),
            'total_neto': Decimal('0')
        }
    }
    
    # Calcular planillas de empleados
    for empleado in empleados:
        pago = calcular_planilla_empleado(empleado, empresa, mes, año)
        
    # Guardar en base de datos
    from app import db
    db.session.add(pago)
        
        resultados['empleados'].append({
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'dni': empleado.dni,
            'sueldo_base': float(empleado.sueldo_base),
            'dias_trabajados': pago.dias_trabajados,
            'dias_faltados': pago.dias_faltados,
            'beneficios': {
                'vacaciones': float(pago.vacaciones),
                'cts': float(pago.cts),
                'gratificacion': float(pago.gratificacion),
                'asignacion_familiar': float(pago.asignacion_familiar)
            },
            'descuentos': {
                'pension': float(pago.pension),
                'impuesto_renta': float(pago.impuesto_renta),
                'prestamos': float(pago.prestamos),
                'adelantos': float(pago.adelantos)
            },
            'total_ingresos': float(pago.total_ingresos),
            'total_descuentos': float(pago.total_descuentos),
            'neto_pagar': float(pago.neto_pagar)
        })
        
        resultados['totales']['total_ingresos'] += pago.total_ingresos
        resultados['totales']['total_descuentos'] += pago.total_descuentos
        resultados['totales']['total_neto'] += pago.neto_pagar
    
    # Calcular planillas de locadores
    for locador in locadores:
        pago_locador = calcular_planilla_locador(locador, mes, año)
        
    # Guardar en base de datos
    from app import db
    db.session.add(pago_locador)
        
        resultados['locadores'].append({
            'id': locador.id,
            'nombres': locador.nombres,
            'apellidos': locador.apellidos,
            'dni': locador.dni,
            'monto_mensual': float(locador.monto_mensual),
            'suspendido': locador.suspendido,
            'monto_bruto': float(pago_locador.monto_bruto),
            'retencion_4ta_cat': float(pago_locador.retencion_4ta_cat),
            'neto_pagar': float(pago_locador.neto_pagar)
        })
        
        resultados['totales']['total_neto'] += pago_locador.neto_pagar
    
    # Actualizar contadores
    resultados['totales']['total_empleados'] = len(empleados)
    resultados['totales']['total_locadores'] = len(locadores)
    
    # Convertir Decimal a float para JSON
    resultados['totales']['total_ingresos'] = float(resultados['totales']['total_ingresos'])
    resultados['totales']['total_descuentos'] = float(resultados['totales']['total_descuentos'])
    resultados['totales']['total_neto'] = float(resultados['totales']['total_neto'])
    
    # Confirmar cambios en base de datos
    from app import db
    db.session.commit()
    
    return resultados

def obtener_resumen_regimen(empresa_id):
    """
    Obtiene un resumen de las reglas aplicables según el régimen laboral
    """
    empresa = Empresa.query.get_or_404(empresa_id)
    regimen = empresa.regimen_laboral
    
    reglas = {
        'microempresa': {
            'vacaciones': '15 días anuales',
            'cts': 'NO corresponde',
            'gratificaciones': 'NO corresponde',
            'asignacion_familiar': 'NO corresponde',
            'descripcion': 'Régimen de Microempresa (REMYPE)'
        },
        'pequeña_empresa': {
            'vacaciones': '15 días anuales',
            'cts': 'Media remuneración anual (15 días por año)',
            'gratificaciones': 'Medio sueldo en Julio y Diciembre',
            'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)',
            'descripcion': 'Régimen de Pequeña Empresa (REMYPE)'
        },
        'general': {
            'vacaciones': '30 días anuales',
            'cts': 'Un sueldo anual',
            'gratificaciones': 'Un sueldo + 9% bonificación en Julio y Diciembre',
            'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)',
            'descripcion': 'Régimen General'
        }
    }
    
    return reglas.get(regimen, reglas['general'])

