import os

class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///sally.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_VERIFICACION = os.environ.get('TOKEN_SALLY', 'SALLY')

    WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')

    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')

    WHATSAPP_API_URL = 'https://graph.facebook.com/v22.0'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'sally-secret-key-change-in-prod')

class TestingConfig(Config):
    """Configuración para pruebas unitarias."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WHATSAPP_ACCESS_TOKEN = 'test-token'
    WHATSAPP_PHONE_NUMBER_ID = 'test-phone-id'