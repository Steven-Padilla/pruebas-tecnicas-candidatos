from orm_models import Profile
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class ProfileService:
    @classmethod
    def get_profiles(cls, service_code):
        try:
            items = []
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                profiles = db_session.query(Profile).filter_by(status = 1).all()

                items = [p.to_dict() for p in profiles]

                return items
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_profile(cls, id, service_code):
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                profile = db_session.query(Profile).filter_by(id=id)

                if profile is None:
                    return {}

                return profile.to_dict()
        except CustomException as ex:
            raise CustomException(ex)