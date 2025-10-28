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
    suspendido = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

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
        if empresa.regimen_laboral in ['microempresa', 'pequeña_empresa']:
            vacaciones = sueldo_base * 15 / 360
        else:
            vacaciones = sueldo_base * 30 / 360
            
        if empresa.regimen_laboral == 'microempresa':
            cts = 0
        elif empresa.regimen_laboral == 'pequeña_empresa':
            cts = sueldo_base * 15 / 12
        else:
            cts = sueldo_base
            
        if empresa.regimen_laboral == 'microempresa':
            gratificacion = 0
        elif empresa.regimen_laboral == 'pequeña_empresa' and mes in [7, 12]:
            gratificacion = sueldo_base / 2
        elif empresa.regimen_laboral == 'general' and mes in [7, 12]:
            gratificacion = sueldo_base * 1.09
        else:
            gratificacion = 0
            
        if empresa.regimen_laboral in ['pequeña_empresa', 'general'] and sueldo_base <= 1025:
            asignacion_familiar = 102.50
        else:
            asignacion_familiar = 0
        
        # Descuentos
        if empleado.tipo_pension == 'ONP':
            pension = sueldo_base * 0.13
        else:
            pension = sueldo_base * 0.12
            
        if sueldo_base > 1025:
            impuesto_renta = max(0, (sueldo_base - 1025) * 0.08)
        else:
            impuesto_renta = 0
        
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
                'vacaciones': round(vacaciones, 2),
                'cts': round(cts, 2),
                'gratificacion': round(gratificacion, 2),
                'asignacion_familiar': round(asignacion_familiar, 2)
            },
            'descuentos': {
                'pension': round(pension, 2),
                'impuesto_renta': round(impuesto_renta, 2),
                'prestamos': 0,
                'adelantos': 0
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
