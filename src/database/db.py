from decouple import config
import requests
from sqlalchemy import create_engine
from src.utils.errors.CustomException import CustomException

def get_connection_servicecode_orm(service_code):
    try:
        data = {'clave': 'issoftware', 'codservicio': service_code}
        external_url = 'https://is-software.net/isadmin/obtenerservidorapp.php'
        response = requests.post(external_url, data=data)

        if response.status_code == 200:
            response_json = response.json()
            db_name = response_json['datosservidor']['db']
            engine = create_engine(f"mysql+pymysql://{config('MYSQL_USER')}:{config('MYSQL_PASSWORD')}@{config('MYSQL_HOST')}/{db_name}", pool_pre_ping=True)
        return engine
    except CustomException as ex:
        raise CustomException(ex)
    
