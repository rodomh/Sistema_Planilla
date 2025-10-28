"""
Configuración de producción para el Sistema de Planillas Multirégimen Perú
"""

import os
from datetime import timedelta

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sispla_peru_2024_production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sispla.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    
    # Configuración de logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'sispla.log'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sispla_dev.db'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sispla_prod.db'
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

