from typing import Any, Union
from orm_models import Users, UsersCentral
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker
from extensions import db

class ExampleService:
    @classmethod
    def get_user_data_with_wallet_amount(cls, user_id: int, service_code:int)-> dict:
        try:
            json_response = {}

            engine = get_connection_servicecode_orm(service_code)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

            #Hay muchas formas de hacer una misma query, utiliza la que mejor se adapte a tu requerimiento
            #En este caso se puede usar filter, filter_by, get, etc etc etc.
            user_central: Union[UsersCentral, Any] = UsersCentral.query.get(user_id)

            if user_central is None:
                # *.__tablename__ es un valor que se establece en todos los modelos
                raise MissingDataException(UsersCentral.__tablename__, user_id, get_db_name_app())

            #Para este caso en particular es probable que el usuario no exista en la bd del club pese a estar en la bd central
            user_club: Union[Users, Any] = db_session.query(Users).get(user_id)
            
            wallet_balance = 0.0

            if user_club is not None:
                wallet_balance = user_club.wallet_balance
            
            json_response = user_central.to_dict(only=('id', 'name', 'lastname', 'secondsurname', 'picture'))
            #Como se mencionó una vez obtenida la información se pueden usar en cualquier estructura de datos, listas, diccionarios, sets, tuplas, etc
            json_response.update({'wallet_balance': wallet_balance}) 

            return json_response
        except CustomException as e:
            raise CustomException(f"Error: {str(e)}") #lo enviará al routes