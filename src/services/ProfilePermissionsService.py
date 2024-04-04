from typing import Any, Union
from orm_models import Permission
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class ProfilePermissionsService:
    @classmethod
    def get_permissions(cls, profile_id, service_code):
        try:
            items = []
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                permissions = db_session.query(Permission).filter_by(profile_id = profile_id, admin = 2).all()

                items = [p.to_dict() for p in permissions]

                return items
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def get_permission_module_by_profile_id(cls, submodule_id, profile_id, service_code, is_user_system_central):
        try:
            if is_user_system_central:
                permission: Union[Permission, Any] = Permission.query.filter(
                    Permission.profile_id == profile_id, 
                    Permission.module_menu_id == submodule_id,
                    Permission.admin == 1
                ).first()
                
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session
                    
                    permission = db_session.query(Permission).filter_by(module_menu_id = submodule_id, profile_id = profile_id, admin = 1).first()

            if permission is None:
                return  {
                    "admin": 1,
                    "delete": 0,
                    "edit": 0,
                    "id": -1,
                    "insert": 0,
                    "module_menu_id": submodule_id,
                    "profile_id": profile_id
                }

            return permission.to_dict(rules=("-module_menu","-profile"))
        except CustomException as ex:
            raise CustomException(ex)