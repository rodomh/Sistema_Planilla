from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sispla_peru_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sispla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importar modelos después de crear db
import models
# Hacer que los modelos usen la instancia de db de app.py
models.db = db
from models import *
from calculadora_planilla import calcular_planilla_completa

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
        resultado = calcular_planilla_completa(empresa_id, mes, año)
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

@app.route('/ausencias/<int:empresa_id>')
def ausencias(empresa_id):
    """Gestión de ausencias por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
    ausencias = Ausencia.query.join(Empleado).filter(Empleado.empresa_id == empresa_id).all()
    return render_template('ausencias.html', empresa=empresa, empleados=empleados, ausencias=ausencias)

@app.route('/deudas/<int:empresa_id>')
def deudas(empresa_id):
    """Gestión de deudas internas por empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id).all()
    prestamos = Prestamo.query.join(Empleado).filter(Empleado.empresa_id == empresa_id).all()
    adelantos = Adelanto.query.join(Empleado).filter(Empleado.empresa_id == empresa_id).all()
    
    return render_template('deudas.html', 
                         empresa=empresa, 
                         empleados=empleados, 
                         locadores=locadores,
                         prestamos=prestamos,
                         adelantos=adelantos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

