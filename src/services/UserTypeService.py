from orm_models import UserType
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class UserTypeService:
    @classmethod
    def get_user_types(cls, service_code):
        try:
            items = []
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                user_types = db_session.query(UserType).all()

                items = [p.to_dict() for p in user_types]

                return items
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_user_type(cls, id, service_code):
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                user_type = db_session.query(UserType).filter_by(id = id).first()

                if user_type is None:
                    return {}

                return user_type.to_dict()
        except CustomException as ex:
            raise CustomException(ex)
