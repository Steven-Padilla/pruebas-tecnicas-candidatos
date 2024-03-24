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
    def get_permission(cls, id_permission, profile_id, service_code):
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                permission = db_session.query(Permission).filter_by(id = id_permission, profile_id = profile_id, admin = 2).first()

                if permission is None:
                    return {}

                return permission.to_dict()
        except CustomException as ex:
            raise CustomException(ex)