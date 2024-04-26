from typing import Any, Union
from sqlalchemy import func, cast
from sqlalchemy.dialects.mysql import CHAR
from orm_models import UsersSystem, Enterprise
from src.database.db import get_connection_servicecode_orm # Database
from src.utils.Security import Security
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException # Errors
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class AuthService():
    @classmethod
    def login_user(cls, username: str, password: str, service_code: int) -> dict:
        """
        Get user (customer) information from 'users' table based on access credentials.

        Args:
            username (str): The customer's username.
            password (str): The customer's password.
            service_code (int): The service code for database connection.

        Returns:
            dict: A dictionary containing the customer information.

        Raises:
            CustomException: If an error occurs during the retrieval process or if the court is not found.
        """
        try:
            #Primero se busca si es un administrador de sistema y en caso contrario será una cuenta del club (cliente)
            user_type = ""
            club_name = get_db_name_app()
            
            user: Union[UsersSystem, Any] = UsersSystem.query.filter(
                    UsersSystem.username == username,
                    UsersSystem.password == password,
                    UsersSystem.service_code == service_code,
                    UsersSystem.status == 1,
                ).first()
            
            if user is not None:
                user_type = "Administrator"
                is_user_system_central = True
                profile_id = user.profile_id
                if user.user_type.is_costumer == 1: #Es cliente
                    club: Union[Enterprise, Any] = Enterprise.query.filter(Enterprise.service_code == service_code).first()
                    if club.status != 1: #Club existente pero sin servicio
                        return {"message": "El club vinculado a esta cuenta está fuera de servicio", "success": False}
                    club_name = club.name
            else:
                clients_service_codes: list[tuple] = Enterprise.query.with_entities(Enterprise.service_code).all()
                clients_service_codes: list[int] = [code for (code,) in clients_service_codes] #se extrae de las tuplas
                if service_code not in clients_service_codes:
                    raise MissingDataException(Enterprise.__tablename__, get_db_name_app())

            if user is None: #Cuenta registrada por el club (cliente) por lo que estará fuera de la central
                user_type = ""
                club: Union[Enterprise, Any] = Enterprise.query.filter(Enterprise.service_code == service_code).first()
                
                if club is None: #Club inexistente
                    raise MissingDataException(Enterprise.__tablename__, get_db_name_app())
                    
                if club.status != 1: #Club existente pero sin servicio
                    return {"message": "El club vinculado a esta cuenta está fuera de servicio", "success": False}

                club_name = club.name
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    db_session: Session

                    user: Union[UsersSystem, Any] = db_session.query(UsersSystem).filter(
                        UsersSystem.username == username,
                        UsersSystem.password == password,
                        UsersSystem.status == 1,
                    ).first()
                    
                if user is None:
                    raise MissingDataException(UsersSystem.__tablename__, engine.url.database)
                is_user_system_central = False
                profile_id = user.profile_id
            
            token = Security.generate_token(user, service_code, is_user_system_central, user_type, profile_id)

            json_response = {
                'token': token, 
                'session': user.service_code, 
                'profile_id': user.profile_id, 
                'club_name': club_name, 
                'success': True
            }

            return json_response
        except CustomException as ex:
            raise CustomException(ex)