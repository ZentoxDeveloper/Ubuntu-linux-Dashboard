import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dashboard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # SMB settings
    BASE_SMB_PATH = os.environ.get('SMB_PATH') or '/mnt/smb'
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Application settings
    MAIN_LOGO_URL = os.environ.get('MAIN_LOGO_URL') or 'https://assets.ubuntu.com/v1/c5cb0f8e-picto-ubuntu.svg'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    
    # Service names
    OPENVPN_SERVICE = 'openvpn'
    SQUID_SERVICE = 'squid'
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
