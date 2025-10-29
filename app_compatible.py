from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sispla_peru_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sispla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos ultra básicos sin herencia compleja
class Empresa(db.Model):
    __tablename__ = 'empresas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    regimen_laboral = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(500))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    sueldo_base = db.Column(db.Float, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(500))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    tipo_pension = db.Column(db.String(20), default='ONP')
    afp_codigo = db.Column(db.String(10))
    cuenta_bancaria = db.Column(db.String(20))
    banco = db.Column(db.String(50))
    tipo_pago = db.Column(db.String(20), default='mensual')  # 'mensual' o 'quincenal'
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Locador(db.Model):
    __tablename__ = 'locadores'
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    monto_mensual = db.Column(db.Float, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    direccion = db.Column(db.String(500))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    cuenta_bancaria = db.Column(db.String(20))
    banco = db.Column(db.String(50))
    suspendido = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Ausencia(db.Model):
    __tablename__ = 'ausencias'
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'falta', 'permiso', 'vacaciones', 'licencia'
    justificada = db.Column(db.Boolean, default=False)
    motivo = db.Column(db.String(500))
    horas_perdidas = db.Column(db.Float, default=8.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con Empleado
    empleado = db.relationship('Empleado', backref='ausencias')

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    monto_pendiente = db.Column(db.Float, nullable=False)
    cuota_mensual = db.Column(db.Float, nullable=False)
    fecha_prestamo = db.Column(db.Date, nullable=False)
    fecha_finalizacion = db.Column(db.Date)
    motivo = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con Empleado
    empleado = db.relationship('Empleado', backref='prestamos')

class Adelanto(db.Model):
    __tablename__ = 'adelantos'
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha_adelanto = db.Column(db.Date, nullable=False)
    mes_aplicar = db.Column(db.Integer, nullable=False)
    año_aplicar = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(500))
    aplicado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con Empleado
    empleado = db.relationship('Empleado', backref='adelantos')

# Rutas principales
@app.route('/')
def index():
    """Página principal del sistema"""
    empresas = Empresa.query.all()
    
    # Calcular conteos de empleados y locadores activos por empresa
    empresas_con_conteos = []
    for empresa in empresas:
        empleados_activos = Empleado.query.filter_by(empresa_id=empresa.id, activo=True).count()
        locadores_activos = Locador.query.filter_by(empresa_id=empresa.id, activo=True).count()
        
        empresas_con_conteos.append({
            'empresa': empresa,
            'empleados_activos': empleados_activos,
            'locadores_activos': locadores_activos
        })
    
    return render_template('index.html', empresas_con_conteos=empresas_con_conteos)

@app.route('/empresas')
def empresas():
    """Gestión de empresas"""
    empresas = Empresa.query.all()
    return render_template('empresas.html', empresas=empresas)

@app.route('/empresa/nueva', methods=['GET', 'POST'])
def nueva_empresa():
    """Crear nueva empresa"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        regimen = request.form['regimen_laboral']
        ruc = request.form['ruc']
        
        empresa = Empresa(
            nombre=nombre,
            regimen_laboral=regimen,
            ruc=ruc
        )
        db.session.add(empresa)
        db.session.commit()
        flash('Empresa creada exitosamente', 'success')
        return redirect(url_for('empresas'))
    
    return render_template('nueva_empresa.html')

@app.route('/personal/<int:empresa_id>')
def personal(empresa_id):
    """Gestión de personal por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id).all()
    return render_template('personal.html', empresa=empresa, empleados=empleados, locadores=locadores)

@app.route('/empleado/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_empleado(empresa_id):
    """Crear nuevo empleado"""
    empresa = Empresa.query.get_or_404(empresa_id)
    
    if request.method == 'POST':
        empleado = Empleado(
            empresa_id=empresa_id,
            nombres=request.form['nombres'],
            apellidos=request.form['apellidos'],
            dni=request.form['dni'],
            sueldo_base=float(request.form['sueldo_base']),
            fecha_ingreso=datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d').date(),
            tipo_pension=request.form['tipo_pension'],
            afp_codigo=request.form.get('afp_codigo', ''),
            cuenta_bancaria=request.form.get('cuenta_bancaria', ''),
            banco=request.form.get('banco', ''),
            tipo_pago=request.form.get('tipo_pago', 'mensual')
        )
        db.session.add(empleado)
        db.session.commit()
        flash('Empleado creado exitosamente', 'success')
        return redirect(url_for('personal', empresa_id=empresa_id))
    
    return render_template('nuevo_empleado.html', empresa=empresa)

@app.route('/locador/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_locador(empresa_id):
    """Crear nuevo locador de servicios"""
    empresa = Empresa.query.get_or_404(empresa_id)
    
    if request.method == 'POST':
        locador = Locador(
            empresa_id=empresa_id,
            nombres=request.form['nombres'],
            apellidos=request.form['apellidos'],
            dni=request.form['dni'],
            monto_mensual=float(request.form['monto_mensual']),
            fecha_inicio=datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date(),
            cuenta_bancaria=request.form.get('cuenta_bancaria', ''),
            banco=request.form.get('banco', ''),
            suspendido=request.form.get('suspendido') == 'on'
        )
        db.session.add(locador)
        db.session.commit()
        flash('Locador creado exitosamente', 'success')
        return redirect(url_for('personal', empresa_id=empresa_id))
    
    return render_template('nuevo_locador.html', empresa=empresa)

@app.route('/planilla/<int:empresa_id>')
def planilla(empresa_id):
    """Vista de planilla por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id).all()
    
    # Obtener mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    return render_template('planilla.html', 
                         empresa=empresa, 
                         empleados=empleados, 
                         locadores=locadores,
                         mes=mes_actual,
                         año=año_actual)

@app.route('/calcular_planilla/<int:empresa_id>', methods=['POST'])
def calcular_planilla(empresa_id):
    """Calcular planilla para una empresa específica"""
    empresa = Empresa.query.get_or_404(empresa_id)
    mes = int(request.form['mes'])
    año = int(request.form['año'])
    
    try:
        resultado = calcular_planilla_simple(empresa_id, mes, año)
        return jsonify({
            'success': True,
            'resultado': resultado,
            'empresa': empresa.nombre,
            'mes': mes,
            'año': año
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def calcular_planilla_simple(empresa_id, mes, año):
    """Función simplificada para calcular planilla"""
    empresa = Empresa.query.get_or_404(empresa_id)
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
            'total_ingresos': 0,
            'total_descuentos': 0,
            'total_neto': 0
        }
    }
    
    # Calcular planillas de empleados
    for empleado in empleados:
        # Cálculo básico
        sueldo_base = float(empleado.sueldo_base)
        
        # Calcular días trabajados (considerando ausencias)
        dias_trabajados = 30  # Días base del mes
        dias_faltados = 0
        horas_perdidas = 0
        
        # Obtener ausencias del empleado en el mes
        ausencias_empleado = db.session.query(Ausencia).filter(
            Ausencia.empleado_id == empleado.id,
            db.extract('month', Ausencia.fecha) == mes,
            db.extract('year', Ausencia.fecha) == año
        ).all()
        
        for ausencia in ausencias_empleado:
            if ausencia.tipo == 'falta' and not ausencia.justificada:
                dias_faltados += 1
                horas_perdidas += ausencia.horas_perdidas
            elif ausencia.tipo == 'permiso' and not ausencia.justificada:
                dias_faltados += 0.5  # Medio día por permiso
                horas_perdidas += ausencia.horas_perdidas
        
        dias_trabajados = 30 - dias_faltados
        
        # Ajustar sueldo base por días trabajados
        sueldo_ajustado = sueldo_base * (dias_trabajados / 30)
        
        # Aplicar tipo de pago (quincenal = 50% del sueldo ajustado)
        if empleado.tipo_pago == 'quincenal':
            sueldo_ajustado = sueldo_ajustado * 0.5
        
        # Beneficios según régimen
        if empresa.regimen_laboral in ['microempresa', 'pequeña_empresa']:
            vacaciones = sueldo_ajustado * 15 / 360
        else:
            vacaciones = sueldo_ajustado * 30 / 360
            
        if empresa.regimen_laboral == 'microempresa':
            cts = 0
        elif empresa.regimen_laboral == 'pequeña_empresa':
            cts = sueldo_ajustado * 15 / 12
        else:
            cts = sueldo_ajustado
            
        if empresa.regimen_laboral == 'microempresa':
            gratificacion = 0
        elif empresa.regimen_laboral == 'pequeña_empresa' and mes in [7, 12]:
            gratificacion = sueldo_ajustado / 2
        elif empresa.regimen_laboral == 'general' and mes in [7, 12]:
            gratificacion = sueldo_ajustado * 1.09
        else:
            gratificacion = 0
            
        if empresa.regimen_laboral in ['pequeña_empresa', 'general'] and sueldo_ajustado <= 1025:
            asignacion_familiar = 102.50
        else:
            asignacion_familiar = 0
        
        # Descuentos por pensión e impuestos
        if empleado.tipo_pension == 'ONP':
            pension = sueldo_ajustado * 0.13
        else:
            pension = sueldo_ajustado * 0.12
            
        if sueldo_ajustado > 1025:
            impuesto_renta = max(0, (sueldo_ajustado - 1025) * 0.08)
        else:
            impuesto_renta = 0
        
        # Descuentos por deudas internas
        prestamos_descuento = 0
        adelantos_descuento = 0
        
        # Obtener préstamos activos del empleado
        prestamos = db.session.query(Prestamo).filter(
            Prestamo.empleado_id == empleado.id,
            Prestamo.activo == True
        ).all()
        
        for prestamo in prestamos:
            prestamos_descuento += prestamo.cuota_mensual
        
        # Obtener adelantos pendientes del empleado para este mes
        adelantos = db.session.query(Adelanto).filter(
            Adelanto.empleado_id == empleado.id,
            Adelanto.mes_aplicar == mes,
            Adelanto.año_aplicar == año,
            Adelanto.aplicado == False
        ).all()
        
        for adelanto in adelantos:
            adelantos_descuento += adelanto.monto
            adelanto.aplicado = True  # Marcar como aplicado
        
        # Totales
        total_ingresos = sueldo_ajustado + vacaciones + cts + gratificacion + asignacion_familiar
        total_descuentos = pension + impuesto_renta + prestamos_descuento + adelantos_descuento
        neto_pagar = total_ingresos - total_descuentos
        
        resultados['empleados'].append({
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'dni': empleado.dni,
            'sueldo_base': sueldo_base,
            'sueldo_ajustado': round(sueldo_ajustado, 2),
            'tipo_pago': empleado.tipo_pago,
            'cuenta_bancaria': empleado.cuenta_bancaria or '',
            'banco': empleado.banco or '',
            'dias_trabajados': round(dias_trabajados, 1),
            'dias_faltados': round(dias_faltados, 1),
            'horas_perdidas': round(horas_perdidas, 1),
            'beneficios': {
                'vacaciones': round(vacaciones, 2),
                'cts': round(cts, 2),
                'gratificacion': round(gratificacion, 2),
                'asignacion_familiar': round(asignacion_familiar, 2)
            },
            'descuentos': {
                'pension': round(pension, 2),
                'impuesto_renta': round(impuesto_renta, 2),
                'prestamos': round(prestamos_descuento, 2),
                'adelantos': round(adelantos_descuento, 2)
            },
            'total_ingresos': round(total_ingresos, 2),
            'total_descuentos': round(total_descuentos, 2),
            'neto_pagar': round(neto_pagar, 2)
        })
        
        resultados['totales']['total_ingresos'] += total_ingresos
        resultados['totales']['total_descuentos'] += total_descuentos
        resultados['totales']['total_neto'] += neto_pagar
    
    # Calcular planillas de locadores
    for locador in locadores:
        monto_bruto = float(locador.monto_mensual)
        if not locador.suspendido and monto_bruto > 1500:
            retencion_4ta_cat = monto_bruto * 0.08
        else:
            retencion_4ta_cat = 0
        neto_pagar = monto_bruto - retencion_4ta_cat
        
        resultados['locadores'].append({
            'id': locador.id,
            'nombres': locador.nombres,
            'apellidos': locador.apellidos,
            'dni': locador.dni,
            'monto_mensual': monto_bruto,
            'suspendido': locador.suspendido,
            'monto_bruto': monto_bruto,
            'retencion_4ta_cat': round(retencion_4ta_cat, 2),
            'neto_pagar': round(neto_pagar, 2)
        })
        
        resultados['totales']['total_neto'] += neto_pagar
    
    # Actualizar contadores
    resultados['totales']['total_empleados'] = len(empleados)
    resultados['totales']['total_locadores'] = len(locadores)
    resultados['totales']['total_ingresos'] = round(resultados['totales']['total_ingresos'], 2)
    resultados['totales']['total_descuentos'] = round(resultados['totales']['total_descuentos'], 2)
    resultados['totales']['total_neto'] = round(resultados['totales']['total_neto'], 2)
    
    return resultados

# Rutas para gestión de ausencias
@app.route('/ausencias/<int:empresa_id>')
def ausencias(empresa_id):
    """Gestión de ausencias por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    # Obtener ausencias del mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    ausencias = db.session.query(Ausencia).join(Empleado).filter(
        Empleado.empresa_id == empresa_id,
        db.extract('month', Ausencia.fecha) == mes_actual,
        db.extract('year', Ausencia.fecha) == año_actual
    ).all()
    
    return render_template('ausencias.html', 
                         empresa=empresa, 
                         empleados=empleados, 
                         ausencias=ausencias,
                         mes=mes_actual,
                         año=año_actual)

@app.route('/ausencia/nueva/<int:empresa_id>', methods=['GET', 'POST'])
def nueva_ausencia(empresa_id):
    """Crear nueva ausencia"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    if request.method == 'POST':
        ausencia = Ausencia(
            empleado_id=int(request.form['empleado_id']),
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d').date(),
            tipo=request.form['tipo'],
            justificada=request.form.get('justificada') == 'on',
            motivo=request.form['motivo'],
            horas_perdidas=float(request.form['horas_perdidas'])
        )
        db.session.add(ausencia)
        db.session.commit()
        flash('Ausencia registrada exitosamente', 'success')
        return redirect(url_for('ausencias', empresa_id=empresa_id))
    
    return render_template('nueva_ausencia.html', empresa=empresa, empleados=empleados)

@app.route('/ausencia/justificar/<int:ausencia_id>', methods=['POST'])
def justificar_ausencia(ausencia_id):
    """Justificar una ausencia"""
    ausencia = Ausencia.query.get_or_404(ausencia_id)
    ausencia.justificada = True
    ausencia.motivo = request.form['motivo']
    db.session.commit()
    flash('Ausencia justificada exitosamente', 'success')
    return redirect(url_for('ausencias', empresa_id=ausencia.empleado.empresa_id))

@app.route('/ausencia/eliminar/<int:ausencia_id>', methods=['POST'])
def eliminar_ausencia(ausencia_id):
    """Eliminar una ausencia"""
    ausencia = Ausencia.query.get_or_404(ausencia_id)
    empresa_id = ausencia.empleado.empresa_id
    db.session.delete(ausencia)
    db.session.commit()
    flash('Ausencia eliminada exitosamente', 'success')
    return redirect(url_for('ausencias', empresa_id=empresa_id))

# Rutas para gestión de deudas internas
@app.route('/deudas/<int:empresa_id>')
def deudas(empresa_id):
    """Gestión de deudas internas por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    # Obtener préstamos activos
    prestamos = db.session.query(Prestamo).join(Empleado).filter(
        Empleado.empresa_id == empresa_id,
        Prestamo.activo == True
    ).all()
    
    # Obtener adelantos pendientes
    adelantos = db.session.query(Adelanto).join(Empleado).filter(
        Empleado.empresa_id == empresa_id,
        Adelanto.aplicado == False
    ).all()
    
    return render_template('deudas.html', 
                         empresa=empresa, 
                         empleados=empleados,
                         prestamos=prestamos,
                         adelantos=adelantos)

@app.route('/prestamo/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_prestamo(empresa_id):
    """Crear nuevo préstamo"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    if request.method == 'POST':
        monto_total = float(request.form['monto_total'])
        cuotas = int(request.form['cuotas'])
        cuota_mensual = monto_total / cuotas
        
        prestamo = Prestamo(
            empleado_id=int(request.form['empleado_id']),
            monto_total=monto_total,
            monto_pendiente=monto_total,
            cuota_mensual=cuota_mensual,
            fecha_prestamo=datetime.strptime(request.form['fecha_prestamo'], '%Y-%m-%d').date(),
            motivo=request.form['motivo']
        )
        db.session.add(prestamo)
        db.session.commit()
        flash('Préstamo creado exitosamente', 'success')
        return redirect(url_for('deudas', empresa_id=empresa_id))
    
    return render_template('nuevo_prestamo.html', empresa=empresa, empleados=empleados)

@app.route('/adelanto/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_adelanto(empresa_id):
    """Crear nuevo adelanto"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    if request.method == 'POST':
        adelanto = Adelanto(
            empleado_id=int(request.form['empleado_id']),
            monto=float(request.form['monto']),
            fecha_adelanto=datetime.strptime(request.form['fecha_adelanto'], '%Y-%m-%d').date(),
            mes_aplicar=int(request.form['mes_aplicar']),
            año_aplicar=int(request.form['año_aplicar']),
            motivo=request.form['motivo']
        )
        db.session.add(adelanto)
        db.session.commit()
        flash('Adelanto creado exitosamente', 'success')
        return redirect(url_for('deudas', empresa_id=empresa_id))
    
    return render_template('nuevo_adelanto.html', empresa=empresa, empleados=empleados)

@app.route('/prestamo/cancelar/<int:prestamo_id>', methods=['POST'])
def cancelar_prestamo(prestamo_id):
    """Cancelar un préstamo"""
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    empresa_id = prestamo.empleado.empresa_id
    prestamo.activo = False
    prestamo.fecha_finalizacion = date.today()
    db.session.commit()
    flash('Préstamo cancelado exitosamente', 'success')
    return redirect(url_for('deudas', empresa_id=empresa_id))

@app.route('/adelanto/cancelar/<int:adelanto_id>', methods=['POST'])
def cancelar_adelanto(adelanto_id):
    """Cancelar un adelanto"""
    adelanto = Adelanto.query.get_or_404(adelanto_id)
    empresa_id = adelanto.empleado.empresa_id
    adelanto.aplicado = True
    db.session.commit()
    flash('Adelanto cancelado exitosamente', 'success')
    return redirect(url_for('deudas', empresa_id=empresa_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
