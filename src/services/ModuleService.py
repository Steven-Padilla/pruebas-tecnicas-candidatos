from typing import Any, Optional, Union
from orm_models import Module, Permission
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db
class ModuleService:
    @classmethod
    def get_modules(cls, user_system_central, service_code):
        try:
            if user_system_central:
                modules = Module.query.filter(Module.admin == 2, Module.status != 2).all()
                if len(modules) == 0:
                    return []
                module_list = [m.to_dict() for m in modules]
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    modules: list[Module] = db_session.query(Module).filter(Module.admin == 2, Module.status != 2).all()
                    
                    module_list = [module_club.to_dict() for module_club in modules]
            return module_list
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def get_module(cls, module_id: int, service_code: int, user_system_central: bool) -> dict:
        try:
            if user_system_central:
                module: Union[Module, Any] = Module.query.filter_by(id = module_id, admin = 2).first()

                if module is None:
                    return {}
                
                json_response = module.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_club: Union[Module, Any] = db_session.query(Module).filter_by(id = module_id, admin = 2).first()

                    if module_club is None:
                        return {}
                    
                    json_response = module_club.to_dict()
            return json_response
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def save_new_module(cls, service_code: int, name: str, status: int, level: int, icon: str, user_system_central: bool) -> dict:
        """
        Save a new module into 'modulos' table.

        Args:
            service_code (int): The service code for database connection.
            name (str): The name of the module.
            status (int): The status value of the module.
            level (int): The level value of the module.
            icon (str): The icon of the module.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the newly created module data.

        Raises:
            CustomException: If an error occurs during the saving process.
        """
        try:
            if user_system_central:
                new_module: Module = Module(
                    name = name,
                    level = level,
                    status = status,
                    icon = icon,
                    admin = 2,
                )
                
                db.session.add(new_module)
                db.session.commit()

                json_response = new_module.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_club: Module = Module(
                        name = name,
                        level = level,
                        status = status,
                        icon = icon,
                        admin = 2,
                    )

                    db_session.add(module_club)
                    db_session.commit()

                    json_response = module_club.to_dict()

            return json_response
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def update_module(cls, module_id: int, service_code: int, user_system_central: bool,
    name: Optional[str] = None, status: Optional[int] = None, level: Optional[int] = None, icon: Optional[str] = None):
        """
        Update a module from 'modulos' table based on ID.

        Args:
            module_id (int):  The ID of the module.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.
            name (Optional[str]): The name of the module (optional).
            status (Optional[int]): The status value of the module (optional).
            level (Optional[int]): The level value of the module (optional).
            icon (Optional[str]): The icon value of the module (optional).
            

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the updating process.
        """
        try:
            if user_system_central:
                module: Union[Module, Any] = Module.query.filter_by(id = module_id).first()
                if module is None:
                    raise MissingDataException(tablename=Module.__tablename__, db_name=get_db_name_app(), id_value=module_id)
                
                cls.update_module_attributes(name, status, level, icon, module)

                db.session.commit()
                module_dict = module.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module: Union[Module, Any] = db_session.query(Module).filter_by(id = module_id).first()
                    
                    if module is None:
                        raise MissingDataException(tablename=Module.__tablename__, db_name=engine.url.database, id_value=module_id)
                    
                    cls.update_module_attributes(name, status, level, icon, module)

                    db_session.commit()

                    module_dict = module.to_dict()
            return module_dict
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def update_module_attributes(cls, name, status, level, icon, module):
        if name is not None and name.strip():
            module.name = name.strip()
        if status is not None:
            module.status = status
        if level is not None:
            module.level = level
        if icon is not None:
            module.icon = icon
    
    @classmethod
    def delete_module(cls, module_id: int, service_code:int, user_system_central: bool) -> dict:
        """
        Delete module from 'modulos' table based on ID.
        
        Args:
            module_id (int): The ID of the module to delete.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the deletion process.
        """
        try:
            if user_system_central:
                module = Module.query.filter_by(id = module_id).first()
                if module is None:
                    return {'message': 'El módulo no existe', 'success': True}
                
                module.status = 2
                db.session.commit()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module = db_session.query(Module).filter_by(id = module_id).first()
                    if module is None:
                        return {'message': 'El módulo no existe', 'success': True}
                    
                    module.status = 2
                    db_session.commit()

            return {'message': 'Módulo eliminado exitosamente', 'success': True}
        except Exception as e:
            print(f'Error: {str(e)}')
            return {'message': f'ERROR: {e}', 'success': False}