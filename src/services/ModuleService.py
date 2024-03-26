from typing import Any, Union
from orm_models import Module, ModuleMenu, Profile, UsersSystem
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class ModuleService:
    @classmethod
    def get_modules(cls, user_system_id, service_code):
        try:
            is_costumer = cls.is_costumer(service_code, user_system_id)

            modules = Module.query.filter_by(admin = 2, status=1).all()
            
            if is_costumer == False:
                if len(modules) == 0:
                    return []
                
                module_list = [m.to_dict() for m in modules]
                return module_list
            
            module_ids_list = [m.id for m in modules] #Lista de ids de modulos activos 

            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                module_menu_club = db_session.query(ModuleMenu).where(ModuleMenu.module_id.in_(module_ids_list)).all()
                module_ids_list = [m.module_id for m in module_menu_club] #Lista de ids de modulos activos en el club
            
                modules = Module.query.where(Module.id.in_(module_ids_list)).all()

                module_menu_list = [m.to_dict() for m in modules]
                return module_menu_list
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def is_costumer(cls, service_code, user_system_id):
        try:
            if user_system_id is not None:
                user_central: Union[UsersSystem, Any] = UsersSystem.query.filter_by(id = user_system_id, service_code = service_code).first()

                if user_central is None:
                    raise MissingDataException(UsersSystem.__tablename__, get_db_name_app(), user_system_id)
                
                return user_central.user_type.is_costumer == 1
            return True
        except Exception as e:
            print(f'Error: {str(e)}')
            return None

    @classmethod
    def get_module(cls, idmodulos):
        try:
            module = Module.query.filter_by(id = idmodulos, admin = 2).first()

            if module is None:
                return {}
            
            json_response = module.to_dict()

            return json_response
        except CustomException as ex:
            raise CustomException(ex)