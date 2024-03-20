from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    USER = config('MYSQL_USER')
    PASSWORD = config('MYSQL_PASSWORD')
    SERVER = config('MYSQL_HOST')
    DB_CENTRAL = config('MYSQL_DB')

    SQLALCHEMY_DATABASE_URI= f"mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DB_CENTRAL}"

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
