from sqlalchemy import func
from extensions import db
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from orm_models import Enterprise, Users, UserEnterprise, UsuarioFavorito
from sqlalchemy.orm import scoped_session, sessionmaker

SERVICE_CODE_BDCENTRAL = 143

class UserFavoriteService():
    @classmethod
    def toggle_favorites(cls, user_id, favorites):
        try:

            engine = get_connection_servicecode_orm(SERVICE_CODE_BDCENTRAL)

            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

            json_response = []
            
            for fav in favorites:
                club_id = fav['club_id']
                status = fav['status']

                favorite = db_session.query(UsuarioFavorito).filter_by(user_id = user_id, club_id = club_id).first()
                if favorite is None:
                    favorite = UsuarioFavorito(user_id = user_id, club_id = club_id)
                    db_session.add(favorite)

                favorite.status = status
                favorite.updated_date = func.now()

            db_session.commit()
            new_favorites =  db_session.query(UsuarioFavorito).filter_by(user_id=user_id).all()
            json_response = [{'club_id' : favorite.club_id, 'status':favorite.status} for favorite in new_favorites]
            db_session.close()
            return json_response
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def get_favorites(cls, user_id):
        try:

            engine = get_connection_servicecode_orm(SERVICE_CODE_BDCENTRAL)

            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

            favorites = db_session.query(UsuarioFavorito).filter_by(user_id=user_id, status=1).all()

            json_response = [{'club_id' : favorite.club_id, 'status':favorite.status} for favorite in favorites]

            db_session.close()

            return json_response
        except CustomException as ex:
            raise CustomException(ex)