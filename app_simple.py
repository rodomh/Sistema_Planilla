#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Planillas Multirégimen - Perú
Versión Simplificada Funcional
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import sqlite3
import io
from openpyxl import Workbook
from werkzeug.utils import secure_filename

# Configuración de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'planillas_peru_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planillas_peru.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crear directorio de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelos simplificados
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
    suspendido = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

# Rutas principales
@app.route('/')
def index():
    """Página principal con resumen de empresas"""
    empresas = Empresa.query.all()
    empresas_con_conteos = []
    
    for empresa in empresas:
        # Contar empleados y locadores activos usando consultas directas
        empleados_activos = db.session.execute(
            db.text("SELECT COUNT(*) FROM empleados WHERE empresa_id = :empresa_id AND activo = 1"),
            {"empresa_id": empresa.id}
        ).scalar()
        
        locadores_activos = db.session.execute(
            db.text("SELECT COUNT(*) FROM locadores WHERE empresa_id = :empresa_id AND activo = 1"),
            {"empresa_id": empresa.id}
        ).scalar()
        
        empresas_con_conteos.append({
            'empresa': empresa,
            'empleados_activos': empleados_activos,
            'locadores_activos': locadores_activos
        })
    
    return render_template('index.html', empresas_con_conteos=empresas_con_conteos)

@app.route('/empresas')
def empresas():
    """Lista de empresas"""
    empresas = Empresa.query.all()
    return render_template('empresas.html', empresas=empresas)

@app.route('/empresa/nueva', methods=['GET', 'POST'])
def nueva_empresa():
    """Crear nueva empresa"""
    if request.method == 'POST':
        try:
            empresa = Empresa(
                nombre=request.form['nombre'],
                ruc=request.form['ruc'],
                regimen_laboral=request.form['regimen_laboral'],
                direccion=request.form.get('direccion', ''),
                telefono=request.form.get('telefono', ''),
                email=request.form.get('email', '')
            )
            db.session.add(empresa)
            db.session.commit()
            flash('Empresa creada exitosamente', 'success')
            return redirect(url_for('empresas'))
        except Exception as e:
            flash(f'Error al crear empresa: {str(e)}', 'error')
    
    return render_template('nueva_empresa.html')

@app.route('/personal/<int:empresa_id>')
def personal(empresa_id):
    """Lista de personal de una empresa"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id, activo=True).all()
    return render_template('personal_simple.html', empresa=empresa, empleados=empleados, locadores=locadores)

@app.route('/empleado/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_empleado(empresa_id):
    """Crear nuevo empleado"""
    empresa = Empresa.query.get_or_404(empresa_id)
    
    if request.method == 'POST':
        try:
            empleado = Empleado(
                empresa_id=empresa_id,
                nombres=request.form['nombres'],
                apellidos=request.form['apellidos'],
                dni=request.form['dni'],
                sueldo_base=float(request.form['sueldo_base']),
                fecha_ingreso=datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d').date(),
                fecha_nacimiento=datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None,
                direccion=request.form.get('direccion', ''),
                telefono=request.form.get('telefono', ''),
                email=request.form.get('email', ''),
                tipo_pension=request.form.get('tipo_pension', 'ONP'),
                afp_codigo=request.form.get('afp_codigo', '') if request.form.get('tipo_pension') == 'AFP' else None
            )
            db.session.add(empleado)
            db.session.commit()
            flash('Empleado creado exitosamente', 'success')
            return redirect(url_for('personal', empresa_id=empresa_id))
        except Exception as e:
            flash(f'Error al crear empleado: {str(e)}', 'error')
    
    return render_template('nuevo_empleado.html', empresa=empresa)

@app.route('/locador/nuevo/<int:empresa_id>', methods=['GET', 'POST'])
def nuevo_locador(empresa_id):
    """Crear nuevo locador"""
    empresa = Empresa.query.get_or_404(empresa_id)
    
    if request.method == 'POST':
        try:
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
        except Exception as e:
            flash(f'Error al crear locador: {str(e)}', 'error')
    
    return render_template('nuevo_locador.html', empresa=empresa)

@app.route('/planilla/<int:empresa_id>')
def planilla(empresa_id):
    """Cálculo de planilla"""
    empresa = Empresa.query.get_or_404(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    return render_template('planilla_simple.html', empresa=empresa, empleados=empleados, locadores=locadores)

@app.route('/calcular_planilla/<int:empresa_id>', methods=['POST'])
def calcular_planilla(empresa_id):
    """Calcular planilla para un mes específico"""
    empresa = Empresa.query.get_or_404(empresa_id)
    mes = int(request.form['mes'])
    año = int(request.form['año'])
    
    # Obtener empleados y locadores activos
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    # Calcular planilla
    resultado = calcular_planilla_simple(empresa_id, mes, año)
    
    return render_template('planilla_simple.html', 
                         empresa=empresa, 
                         empleados=empleados, 
                         locadores=locadores,
                         resultado=resultado,
                         mes=mes,
                         año=año)

def calcular_planilla_simple(empresa_id, mes, año):
    """Función simplificada de cálculo de planilla"""
    empresa = Empresa.query.get(empresa_id)
    empleados = Empleado.query.filter_by(empresa_id=empresa_id, activo=True).all()
    locadores = Locador.query.filter_by(empresa_id=empresa_id, activo=True).all()
    
    resultado = {
        'empresa': empresa,
        'mes': mes,
        'año': año,
        'empleados': [],
        'locadores': [],
        'totales': {
            'total_ingresos': 0,
            'total_descuentos': 0,
            'total_neto': 0
        }
    }
    
    # Calcular para empleados
    for empleado in empleados:
        sueldo_base = empleado.sueldo_base
        
        # Calcular beneficios según régimen
        if empresa.regimen_laboral == 'microempresa':
            vacaciones = 0
            cts = 0
            gratificacion = 0
            asignacion_familiar = 0
        elif empresa.regimen_laboral == 'pequeña_empresa':
            vacaciones = sueldo_base * 15 / 365
            cts = sueldo_base * 15 / 365
            gratificacion = sueldo_base * 0.5 if mes in [7, 12] else 0
            asignacion_familiar = 102.50 if sueldo_base <= 1025 else 0
        else:  # régimen general
            vacaciones = sueldo_base * 30 / 365
            cts = sueldo_base
            gratificacion = sueldo_base * 1.09 if mes in [7, 12] else 0
            asignacion_familiar = 102.50 if sueldo_base <= 1025 else 0
        
        # Calcular descuentos
        pension = sueldo_base * 0.13 if empleado.tipo_pension == 'ONP' else sueldo_base * 0.12
        impuesto_renta = max(0, (sueldo_base - 1025) * 0.08) if sueldo_base > 1025 else 0
        
        total_ingresos = sueldo_base + vacaciones + cts + gratificacion + asignacion_familiar
        total_descuentos = pension + impuesto_renta
        neto = total_ingresos - total_descuentos
        
        resultado['empleados'].append({
            'empleado': empleado,
            'sueldo_base': sueldo_base,
            'vacaciones': vacaciones,
            'cts': cts,
            'gratificacion': gratificacion,
            'asignacion_familiar': asignacion_familiar,
            'pension': pension,
            'impuesto_renta': impuesto_renta,
            'total_ingresos': total_ingresos,
            'total_descuentos': total_descuentos,
            'neto': neto
        })
        
        resultado['totales']['total_ingresos'] += total_ingresos
        resultado['totales']['total_descuentos'] += total_descuentos
        resultado['totales']['total_neto'] += neto
    
    # Calcular para locadores
    for locador in locadores:
        monto_base = locador.monto_mensual
        retencion_4ta = monto_base * 0.08 if not locador.suspendido and monto_base > 1500 else 0
        
        total_ingresos = monto_base
        total_descuentos = retencion_4ta
        neto = total_ingresos - total_descuentos
        
        resultado['locadores'].append({
            'locador': locador,
            'monto_base': monto_base,
            'retencion_4ta': retencion_4ta,
            'total_ingresos': total_ingresos,
            'total_descuentos': total_descuentos,
            'neto': neto
        })
        
        resultado['totales']['total_ingresos'] += total_ingresos
        resultado['totales']['total_descuentos'] += total_descuentos
        resultado['totales']['total_neto'] += neto
    
    return resultado

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)