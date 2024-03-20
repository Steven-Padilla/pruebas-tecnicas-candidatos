from decouple import config
from urllib.parse import quote_plus

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    USER = config('MYSQL_USER')
    PASSWORD = config('MYSQL_PASSWORD')
    SERVER = config('MYSQL_HOST')
    DB_CENTRAL = config('MYSQL_DB')

    password_encoded = quote_plus(PASSWORD)

    SQLALCHEMY_DATABASE_URI= f"mysql+pymysql://{USER}:{password_encoded}@{SERVER}/{DB_CENTRAL}"

    print(SQLALCHEMY_DATABASE_URI)

    SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 280,
    'pool_pre_ping': True
    }
    DEBUG = True

class DeployConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'deploy': DeployConfig
}
