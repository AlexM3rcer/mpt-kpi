import os
from pathlib import Path
from sqlalchemy.engine import URL


class Config:
    PORT = os.getenv('BACKEND_PORT', 8000)
    DEBUG = os.getenv('DEBUG', True)

    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')

    DATABASE_USER: str = os.getenv('DATABASE_USER', 'mpt-kpi')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD', 'C2nrpDBz6Nve')
    DATABASE_HOST: str = os.getenv('DATABASE_HOST', 'db')
    DATABASE_NAME: str = os.getenv('DATABASE_NAME', 'mpt-kpi')
    DATABASE_PORT: int = int(os.getenv('DATABASE_PORT', 3306))

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername='mysql+mysqldb',
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    BASE_DIR = Path(__file__).resolve().parent
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = 'media/'
