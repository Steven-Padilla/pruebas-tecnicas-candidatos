from typing import Any, Optional, Union
from orm_models import UserType
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class UserTypeService:
    @classmethod
    def get_user_types(cls, service_code: int, user_system_central:bool) -> list:
        """
        Get a list of user types information from 'usuarios_sistema' table.

        Args:
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            list: A list containing the user types information.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                user_types = UserType.query.filter(UserType.status != 2).all()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    user_types = db_session.query(UserType).filter(UserType.status != 2).all()

            items = [user_type.to_dict() for user_type in user_types]

            return items
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_user_type(cls, user_type_id: int, service_code: int, user_system_central: bool)-> dict:
        """
        Get user type information from 'tipousuario' table based on ID.

        Args:
            user_id (int): The ID of the user type.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the user type information.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                user_type = UserType.query.filter_by(id = user_type_id).first()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    user_type = db_session.query(UserType).filter_by(id = user_type_id).first()

            if user_type is None:
                return {}

            return user_type.to_dict()
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def save_user_type(cls, service_code: int, name: str, show_on_app: int, status: int, default: int, access_system: int, is_costumer: int, user_system_central: bool) -> dict:
        """
        Save a new user type into 'tipousuario' table.

        Args:
            service_code (int): The service code for database connection.
            name (str): The name of the user type.
            show_on_app (int): The show_on_app value of the user type.
            status (int): The status value of the user type.
            default (int): The default value of the user type.
            access_system (int): The access_system value of the user type.
            is_costumer (int): The is_costumer value of the user type.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the newly created user type data.

        Raises:
            CustomException: If an error occurs during the saving process.
        """
        try:
            new_user_type: UserType = UserType(
                name = name, 
                show_on_app = show_on_app,
                status = status,
                default = default,
                access_system = access_system,
                is_costumer = is_costumer
            )

            if user_system_central:    
                db.session.add(new_user_type)
                db.session.commit()
                new_user_type_dict = new_user_type.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    new_user_type.show_on_app = 0 #only user types can be created for use by the administrator.
                    
                    db_session.add(new_user_type)
                    db_session.commit()
                    new_user_type_dict = new_user_type.to_dict()

            return new_user_type_dict
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def update_user_type(cls, user_type_id: int, service_code: int, user_system_central: bool, 
        name: Optional[str] = None, show_on_app: Optional[int] = None, status: Optional[int] = None, 
        default: Optional[int] = None, access_system: Optional[int] = None, is_costumer: Optional[int] = None) -> dict:
        """
        Update a user type from 'tipousuario' table based on ID.

        Args:
            user_type_id (int):  The ID of the user type.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.
            name (Optional[str]): The name of the user type (optional).
            show_on_app (Optional[int]): The show_on_app value of the user type (optional).
            status (Optional[int]): The status value of the user type (optional).
            default (Optional[int]): The default value of the user type (optional).
            access_system (Optional[int]): The access_system value of the user type (optional).
            is_costumer (Optional[int]): The is_costumer value of the user type (optional).

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the updating process.
        """
        try:
            if user_system_central:
                user_type = UserType.query.filter_by(id = user_type_id).first()
                if user_type is None:
                    raise MissingDataException(tablename=UserType.__tablename__, db_name=get_db_name_app(), id_value=user_type_id)

                cls.update_user_type_attributes(name, show_on_app, default, access_system, is_costumer, status, user_type)
                
                db.session.commit()

                updated_user = user_type.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    user_type = db_session.query(UserType).filter_by(id = user_type_id).first()
                    if user_type is None:
                        raise MissingDataException(tablename=UserType.__tablename__, db_name=engine.url.database, id_value=user_type_id)                

                    cls.update_user_type_attributes(name, show_on_app, default, access_system, is_costumer, status, user_type)

                    db_session.commit()

                    updated_user = user_type.to_dict()
            
            return updated_user
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def update_user_type_attributes(cls, name: Union[None, str], show_on_app: Union[None, int], default: Union[None, int], access_system: Union[None, int], is_costumer: Union[None, int], status: Union[None, int], user_type: UserType):    
        if name is not None and name.strip():
            user_type.name = name.strip()
        if show_on_app is not None:
            user_type.show_on_app = show_on_app
        if default is not None:
            user_type.default = default
        if access_system is not None:
            user_type.access_system = access_system
        if is_costumer is not None:
            user_type.is_costumer = is_costumer
        if status is not None:
            user_type.status = status
    
    @classmethod
    def delete_user_type(cls, user_type_id: int, service_code:int, user_system_central: bool) -> dict:
        """
        Delete user type from 'tipousuario' table based on ID.
        
        Args:
            user_type_id (int): The ID of the user type to delete.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the deletion process.
        """
        try:
            if user_system_central:
                user_type = UserType.query.filter_by(id = user_type_id).first()
                if user_type is None:
                    return {'message': 'El tipo de usuario no existe', 'success': True}
                
                user_type.status = 2 #deleted status
                db.session.commit()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    user_type = db_session.query(UserType).filter_by(id = user_type_id).first()
                    if user_type is None:
                        return {'message': 'El tipo de usuario no existe', 'success': True}
                    
                    user_type.status = 2 #deleted status
                    db_session.commit()

            return {'message': 'Tipo de usuario eliminado exitosamente', 'success': True}
        except Exception as e:
            print(f'Error: {str(e)}')
            return {'message': f'ERROR: {e}', 'success': False}