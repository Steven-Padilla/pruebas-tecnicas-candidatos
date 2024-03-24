from orm_models import Module, ModuleMenuClub
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class ModuleService:
    @classmethod
    def get_modules(cls, user_central, service_code):
        try:
            modules = Module.query.filter_by(admin = 2, status=1).all()
            if len(modules) == 0:
                return []
            
            if user_central:
                module_list = [m.to_dict() for m in modules]
                return module_list
            
            module_ids_list = [m.id for m in modules] #Lista de ids de modulos activos 

            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                module_menu_club = db_session.query(ModuleMenuClub).where(ModuleMenuClub.module_id.in_(module_ids_list)).all()
                module_ids_list = [m.module_id for m in module_menu_club] #Lista de ids de modulos activos en el club
            
                modules = Module.query.where(Module.id.in_(module_ids_list)).all()

            module_menu_list = [m.to_dict() for m in modules]
            return module_menu_list
        except CustomException as ex:
            raise CustomException(ex)

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