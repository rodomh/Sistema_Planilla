from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sispla_peru_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sispla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos que coinciden exactamente con la base de datos existente
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
        sueldo_ajustado = sueldo_base
        
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
        
        # Descuentos
        if empleado.tipo_pension == 'ONP':
            pension = sueldo_ajustado * 0.13
        else:
            pension = sueldo_ajustado * 0.12
            
        if sueldo_ajustado > 1025:
            impuesto_renta = max(0, (sueldo_ajustado - 1025) * 0.08)
        else:
            impuesto_renta = 0
        
        # Totales
        total_ingresos = sueldo_ajustado + vacaciones + cts + gratificacion + asignacion_familiar
        total_descuentos = pension + impuesto_renta
        neto_pagar = total_ingresos - total_descuentos
        
        resultados['empleados'].append({
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'dni': empleado.dni,
            'sueldo_base': sueldo_base,
            'sueldo_ajustado': round(sueldo_ajustado, 2),
            'dias_trabajados': 30,
            'dias_faltados': 0,
            'horas_perdidas': 0,
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

@app.route('/exportar_excel/<int:empresa_id>', methods=['POST'])
def exportar_excel(empresa_id):
    """Exportar planilla a Excel"""
    empresa = Empresa.query.get_or_404(empresa_id)
    mes = int(request.form['mes'])
    año = int(request.form['año'])
    
    try:
        resultado = calcular_planilla_simple(empresa_id, mes, año)
        
        # Crear libro de trabajo
        wb = Workbook()
        
        # Hoja de empleados
        ws_empleados = wb.active
        ws_empleados.title = "Empleados"
        
        # Encabezados para empleados
        headers_empleados = [
            'Nombres', 'Apellidos', 'DNI', 'Sueldo Base', 'Sueldo Ajustado',
            'Días Trabajados', 'Días Faltados', 'Horas Perdidas',
            'Vacaciones', 'CTS', 'Gratificación', 'Asignación Familiar',
            'Pensión', 'Impuesto Renta', 'Préstamos', 'Adelantos', 'Faltas',
            'Total Ingresos', 'Total Descuentos', 'Neto a Pagar'
        ]
        
        # Escribir encabezados
        for col, header in enumerate(headers_empleados, 1):
            cell = ws_empleados.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Escribir datos de empleados
        for row, emp in enumerate(resultado['empleados'], 2):
            ws_empleados.cell(row=row, column=1, value=emp['nombres'])
            ws_empleados.cell(row=row, column=2, value=emp['apellidos'])
            ws_empleados.cell(row=row, column=3, value=emp['dni'])
            ws_empleados.cell(row=row, column=4, value=emp['sueldo_base'])
            ws_empleados.cell(row=row, column=5, value=emp['sueldo_ajustado'])
            ws_empleados.cell(row=row, column=6, value=emp['dias_trabajados'])
            ws_empleados.cell(row=row, column=7, value=emp['dias_faltados'])
            ws_empleados.cell(row=row, column=8, value=emp['horas_perdidas'])
            ws_empleados.cell(row=row, column=9, value=emp['beneficios']['vacaciones'])
            ws_empleados.cell(row=row, column=10, value=emp['beneficios']['cts'])
            ws_empleados.cell(row=row, column=11, value=emp['beneficios']['gratificacion'])
            ws_empleados.cell(row=row, column=12, value=emp['beneficios']['asignacion_familiar'])
            ws_empleados.cell(row=row, column=13, value=emp['descuentos']['pension'])
            ws_empleados.cell(row=row, column=14, value=emp['descuentos']['impuesto_renta'])
            ws_empleados.cell(row=row, column=15, value=emp['descuentos']['prestamos'])
            ws_empleados.cell(row=row, column=16, value=emp['descuentos']['adelantos'])
            ws_empleados.cell(row=row, column=17, value=emp.get('faltas', 0))
            ws_empleados.cell(row=row, column=18, value=emp['total_ingresos'])
            ws_empleados.cell(row=row, column=19, value=emp['total_descuentos'])
            ws_empleados.cell(row=row, column=20, value=emp['neto_pagar'])
        
        # Ajustar ancho de columnas
        for column in ws_empleados.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws_empleados.column_dimensions[column_letter].width = adjusted_width
        
        # Hoja de locadores
        ws_locadores = wb.create_sheet("Locadores")
        
        # Encabezados para locadores
        headers_locadores = [
            'Nombres', 'Apellidos', 'DNI', 'Monto Mensual', 'Suspendido',
            'Retención 4ta Cat', 'Neto a Pagar'
        ]
        
        # Escribir encabezados
        for col, header in enumerate(headers_locadores, 1):
            cell = ws_locadores.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Escribir datos de locadores
        for row, loc in enumerate(resultado['locadores'], 2):
            ws_locadores.cell(row=row, column=1, value=loc['nombres'])
            ws_locadores.cell(row=row, column=2, value=loc['apellidos'])
            ws_locadores.cell(row=row, column=3, value=loc['dni'])
            ws_locadores.cell(row=row, column=4, value=loc['monto_mensual'])
            ws_locadores.cell(row=row, column=5, value='Sí' if loc['suspendido'] else 'No')
            ws_locadores.cell(row=row, column=6, value=loc['retencion_4ta_cat'])
            ws_locadores.cell(row=row, column=7, value=loc['neto_pagar'])
        
        # Ajustar ancho de columnas
        for column in ws_locadores.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws_locadores.column_dimensions[column_letter].width = adjusted_width
        
        # Hoja de resumen
        ws_resumen = wb.create_sheet("Resumen")
        
        # Escribir resumen
        ws_resumen.cell(row=1, column=1, value="Concepto").font = Font(bold=True)
        ws_resumen.cell(row=1, column=2, value="Valor").font = Font(bold=True)
        
        resumen_data = [
            ("Empresa", resultado['empresa']),
            ("Régimen Laboral", resultado['regimen_laboral']),
            ("Período", f"{mes:02d}/{año}"),
            ("Total Empleados", resultado['totales']['total_empleados']),
            ("Total Locadores", resultado['totales']['total_locadores']),
            ("Total Ingresos", resultado['totales']['total_ingresos']),
            ("Total Descuentos", resultado['totales']['total_descuentos']),
            ("Total Neto", resultado['totales']['total_neto'])
        ]
        
        for row, (concepto, valor) in enumerate(resumen_data, 2):
            ws_resumen.cell(row=row, column=1, value=concepto)
            ws_resumen.cell(row=row, column=2, value=valor)
        
        # Ajustar ancho de columnas
        for column in ws_resumen.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 20)
            ws_resumen.column_dimensions[column_letter].width = adjusted_width
        
        # Guardar en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Crear respuesta
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename=planilla_{empresa.nombre}_{mes:02d}_{año}.xlsx'
        
        return response
        
    except Exception as e:
        flash(f'Error al exportar: {str(e)}', 'error')
        return redirect(url_for('planilla', empresa_id=empresa_id))

if __name__ == '__main__':
    # No crear tablas, usar las existentes
    app.run(debug=True, host='0.0.0.0', port=5000)
