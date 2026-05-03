import os

class Config:

    _db_url = os.environ.get('DATABASE_URL', '')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///sally.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_VERIFICACION = os.environ.get('TOKEN_SALLY', 'SALLY')

    WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')

    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')

    WHATSAPP_API_URL = 'https://graph.facebook.com/v25.0'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'sally-secret-key-change-in-prod')

class TestingConfig(Config):
    """Configuración para pruebas unitarias."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WHATSAPP_ACCESS_TOKEN = 'test-token'
    WHATSAPP_PHONE_NUMBER_ID = 'test-phone-id'