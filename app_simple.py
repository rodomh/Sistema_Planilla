from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sispla_peru_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sispla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir modelos directamente aquí para evitar problemas de importación circular
class Empresa(db.Model):
    """Modelo para empresas con régimen laboral específico"""
    __tablename__ = 'empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    regimen_laboral = db.Column(db.String(50), nullable=False)  # 'microempresa', 'pequeña_empresa', 'general'
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)
    
    # Relaciones
    empleados = db.relationship('Empleado', backref='empresa', lazy=True, cascade='all, delete-orphan')
    locadores = db.relationship('Locador', backref='empresa', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Empresa {self.nombre} - {self.regimen_laboral}>'

class Empleado(db.Model):
    """Modelo para empleados con sueldo fijo mensual"""
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    sueldo_base = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    # Configuración de pensiones
    tipo_pension = db.Column(db.String(20), default='ONP')  # 'ONP' o 'AFP'
    afp_codigo = db.Column(db.String(10))  # Código de AFP si aplica
    
    # Estado
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ausencias = db.relationship('Ausencia', backref='empleado', lazy=True, cascade='all, delete-orphan')
    prestamos = db.relationship('Prestamo', backref='empleado', lazy=True, cascade='all, delete-orphan')
    adelantos = db.relationship('Adelanto', backref='empleado', lazy=True, cascade='all, delete-orphan')
    pagos = db.relationship('Pago', backref='empleado', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Empleado {self.nombres} {self.apellidos}>'

class Locador(db.Model):
    """Modelo para locadores de servicios (Recibos por Honorarios)"""
    __tablename__ = 'locadores'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), nullable=False)
    monto_mensual = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    
    # Estado
    suspendido = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    pagos = db.relationship('PagoLocador', backref='locador', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Locador {self.nombres} {self.apellidos}>'

class Ausencia(db.Model):
    """Modelo para registrar ausencias, permisos y faltas"""
    __tablename__ = 'ausencias'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'falta', 'permiso', 'vacaciones', 'licencia'
    justificada = db.Column(db.Boolean, default=False)
    motivo = db.Column(db.Text)
    horas_perdidas = db.Column(db.Numeric(4, 2), default=8.0)  # Horas de trabajo perdidas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ausencia {self.empleado.nombres} - {self.fecha}>'

class Prestamo(db.Model):
    """Modelo para préstamos internos a empleados"""
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto_total = db.Column(db.Numeric(10, 2), nullable=False)
    monto_pendiente = db.Column(db.Numeric(10, 2), nullable=False)
    cuota_mensual = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_prestamo = db.Column(db.Date, nullable=False)
    fecha_finalizacion = db.Column(db.Date)
    motivo = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prestamo {self.empleado.nombres} - S/. {self.monto_total}>'

class Adelanto(db.Model):
    """Modelo para adelantos de sueldo"""
    __tablename__ = 'adelantos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_adelanto = db.Column(db.Date, nullable=False)
    mes_aplicar = db.Column(db.Integer, nullable=False)  # Mes en que se descuenta
    año_aplicar = db.Column(db.Integer, nullable=False)  # Año en que se descuenta
    motivo = db.Column(db.Text)
    aplicado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Adelanto {self.empleado.nombres} - S/. {self.monto}>'

class Pago(db.Model):
    """Modelo para pagos de empleados (quincenales y mensuales)"""
    __tablename__ = 'pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    año = db.Column(db.Integer, nullable=False)
    tipo_pago = db.Column(db.String(20), nullable=False)  # 'quincenal', 'mensual'
    
    # Cálculos base
    sueldo_base = db.Column(db.Numeric(10, 2), nullable=False)
    dias_trabajados = db.Column(db.Integer, default=30)
    dias_faltados = db.Column(db.Integer, default=0)
    
    # Beneficios sociales (según régimen)
    vacaciones = db.Column(db.Numeric(10, 2), default=0)
    cts = db.Column(db.Numeric(10, 2), default=0)
    gratificacion = db.Column(db.Numeric(10, 2), default=0)
    asignacion_familiar = db.Column(db.Numeric(10, 2), default=0)
    
    # Descuentos
    pension = db.Column(db.Numeric(10, 2), default=0)
    impuesto_renta = db.Column(db.Numeric(10, 2), default=0)
    prestamos = db.Column(db.Numeric(10, 2), default=0)
    adelantos = db.Column(db.Numeric(10, 2), default=0)
    otros_descuentos = db.Column(db.Numeric(10, 2), default=0)
    
    # Totales
    total_ingresos = db.Column(db.Numeric(10, 2), nullable=False)
    total_descuentos = db.Column(db.Numeric(10, 2), nullable=False)
    neto_pagar = db.Column(db.Numeric(10, 2), nullable=False)
    
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_pago = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Pago {self.empleado.nombres} - {self.mes}/{self.año}>'

class PagoLocador(db.Model):
    """Modelo para pagos a locadores de servicios"""
    __tablename__ = 'pagos_locadores'
    
    id = db.Column(db.Integer, primary_key=True)
    locador_id = db.Column(db.Integer, db.ForeignKey('locadores.id'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    año = db.Column(db.Integer, nullable=False)
    
    # Cálculos
    monto_bruto = db.Column(db.Numeric(10, 2), nullable=False)
    retencion_4ta_cat = db.Column(db.Numeric(10, 2), default=0)
    neto_pagar = db.Column(db.Numeric(10, 2), nullable=False)
    
    fecha_calculo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_pago = db.Column(db.Date)
    
    def __repr__(self):
        return f'<PagoLocador {self.locador.nombres} - {self.mes}/{self.año}>'

class Configuracion(db.Model):
    """Modelo para configuraciones del sistema"""
    __tablename__ = 'configuraciones'
    
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Configuracion {self.clave}: {self.valor}>'

# Rutas principales
@app.route('/')
def index():
    """Página principal del sistema"""
    empresas = Empresa.query.all()
    return render_template('index.html', empresas=empresas)

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
            afp_codigo=request.form.get('afp_codigo', '')
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
        
        # Beneficios según régimen
        vacaciones = sueldo_base * 15 / 360 if empresa.regimen_laboral in ['microempresa', 'pequeña_empresa'] else sueldo_base * 30 / 360
        cts = 0 if empresa.regimen_laboral == 'microempresa' else sueldo_base * 15 / 12 if empresa.regimen_laboral == 'pequeña_empresa' else sueldo_base
        gratificacion = 0 if empresa.regimen_laboral == 'microempresa' else sueldo_base / 2 if empresa.regimen_laboral == 'pequeña_empresa' and mes in [7, 12] else sueldo_base * 1.09 if empresa.regimen_laboral == 'general' and mes in [7, 12] else 0
        asignacion_familiar = 102.50 if empresa.regimen_laboral in ['pequeña_empresa', 'general'] and sueldo_base <= 1025 else 0
        
        # Descuentos
        pension = sueldo_base * 0.13 if empleado.tipo_pension == 'ONP' else sueldo_base * 0.12
        impuesto_renta = max(0, (sueldo_base - 1025) * 0.08) if sueldo_base > 1025 else 0
        
        # Totales
        total_ingresos = sueldo_base + vacaciones + cts + gratificacion + asignacion_familiar
        total_descuentos = pension + impuesto_renta
        neto_pagar = total_ingresos - total_descuentos
        
        resultados['empleados'].append({
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'dni': empleado.dni,
            'sueldo_base': sueldo_base,
            'dias_trabajados': 30,
            'dias_faltados': 0,
            'beneficios': {
                'vacaciones': vacaciones,
                'cts': cts,
                'gratificacion': gratificacion,
                'asignacion_familiar': asignacion_familiar
            },
            'descuentos': {
                'pension': pension,
                'impuesto_renta': impuesto_renta,
                'prestamos': 0,
                'adelantos': 0
            },
            'total_ingresos': total_ingresos,
            'total_descuentos': total_descuentos,
            'neto_pagar': neto_pagar
        })
        
        resultados['totales']['total_ingresos'] += total_ingresos
        resultados['totales']['total_descuentos'] += total_descuentos
        resultados['totales']['total_neto'] += neto_pagar
    
    # Calcular planillas de locadores
    for locador in locadores:
        monto_bruto = float(locador.monto_mensual)
        retencion_4ta_cat = monto_bruto * 0.08 if not locador.suspendido and monto_bruto > 1500 else 0
        neto_pagar = monto_bruto - retencion_4ta_cat
        
        resultados['locadores'].append({
            'id': locador.id,
            'nombres': locador.nombres,
            'apellidos': locador.apellidos,
            'dni': locador.dni,
            'monto_mensual': monto_bruto,
            'suspendido': locador.suspendido,
            'monto_bruto': monto_bruto,
            'retencion_4ta_cat': retencion_4ta_cat,
            'neto_pagar': neto_pagar
        })
        
        resultados['totales']['total_neto'] += neto_pagar
    
    # Actualizar contadores
    resultados['totales']['total_empleados'] = len(empleados)
    resultados['totales']['total_locadores'] = len(locadores)
    
    return resultados

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
