from datetime import datetime, date
from decimal import Decimal

# db será importado desde app.py

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

