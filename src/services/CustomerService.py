from typing import Any, Union

from flask import jsonify
from orm_models import UserEnterprise, Users, UsersCentral, Enterprise
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class CustomerService:
    @classmethod
    def get_all_users(cls, service_code:int)-> dict:

        try:
            json_response = {}
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session
                users_club: Union[Users, Any] = db_session.query(Users).all()

                if not users_club:
                    return jsonify({'data': [], 'success': True})
                items = [u.id for u in users_club] 
                
                users_central = UsersCentral.query.filter(
                            UsersCentral.id.in_(items),
                            UsersCentral.status == 1
                        ).all()
                if not users_central:
                    raise MissingDataException(UsersCentral.__tablename__, get_db_name_app(),)
                users_actives = [u.as_dict() for u in users_central] 

                json_response = users_actives

                return json_response
        except CustomException as e:
            raise CustomException(f"Error: {str(e)}") #lo enviará al routes
    @classmethod
    def get_user_by_id(cls, service_code:int, id:int)-> dict:

        try:
            json_response = {}
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session

                user_central = UsersCentral.query.filter_by(id=id, status=1).first()
                
                if not user_central:
                    raise MissingDataException(UsersCentral.__tablename__, get_db_name_app(),)
                user = user_central.as_dict() 

                json_response = user

                return json_response
        except CustomException as e:
            raise CustomException(f"Error: {str(e)}") #lo enviará al routes
    @classmethod
    def update_user(cls, user, name, last_name, cellphone, id, password, sex, email) -> dict:
            try:
                json_response = {}

                user_central: Union[UsersCentral, Any] = UsersCentral.query.filter_by(id=id, status=1).first()
                if user_central is None:
                    raise MissingDataException(UsersCentral.__tablename__, get_db_name_app(),)

                if name is not None and name.strip():
                    user_central.name = name
                if last_name is not None and last_name.strip():
                    user_central.lastname = last_name
                if user is not None and user.strip():
                    user_central.user = user
                if cellphone is not None and cellphone.strip():
                    user_central.cellphone = cellphone
                if password is not None and password.strip():
                    user_central.password = password
                if email is not None and email.strip():
                    user_central.email = email
                if sex is not None and sex.strip():
                    user_central.sex = sex

                db.session.commit()
                usuario = user_central.as_dict()
                    
                json_response = usuario
                return json_response
            except CustomException as ex:
                print(f"error: {str(ex)}")
                return CustomException(ex)  

    @classmethod
    def search_cellphone(cls,service_code, cellphone ) -> dict:
        try:
            user_central = UsersCentral.query.filter_by(cellphone=cellphone).first()
            
            if user_central is None:
                return {"user": {}, "edit": False}
            
            engine= get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session
                user_club: Union[Users, Any] = db_session.query(Users).filter_by(id = user_central.id).first() 
                
                if user_club is None:
                    user_central = UsersCentral.query.filter_by(cellphone=cellphone).first()
                    return {"user": user_central.as_dict(), "edit": False}
                
            return {"user": user_central.as_dict(), "edit": True}
        except CustomException as ex:
            print(str(ex))
            return CustomException(ex) 

    @classmethod
    def search_and_create_by_cellphone(cls,service_code, cellphone ) -> dict:
            try:
                json_response = {} 
                wallet_balance = 0.0       
                user_central = UsersCentral.query.filter_by(cellphone=cellphone).first()
                if user_central is None:
                    new_user = UsersCentral(cellphone=cellphone)

                    db.session.add(new_user)
                    db.session.commit()
  
                    cls.create_user_in_club(service_code, wallet_balance, new_user.id )  
                    return new_user.as_dict()
                else:
                    id = user_central.id
                    engine= get_connection_servicecode_orm(service_code)
                    with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                        db_session: Session
                        user_club: Union[Users, Any] = db_session.query(Users).filter_by(id = id).first()

                        if user_club is None:
                            cls.create_user_in_club(service_code, wallet_balance, id)   
                             
                return user_central.as_dict()
                        
            except CustomException as ex:
                print(str(ex))
                return CustomException(ex)  
    @classmethod
    def create_user_in_club(cls, service_code, wallet_balance, id) -> dict:
        try:
            club: Union[Enterprise, Any] = Enterprise.query.filter_by(service_code = service_code).first()
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session
                
                new_user = Users(wallet_balance=wallet_balance, id=id)
                user_enterprise: Union[UserEnterprise, Any] = UserEnterprise.query.filter_by(user_id=id, club_id=club.id, user_type_id=3).first()
                if user_enterprise is None:

                    new_user_interprise = UserEnterprise(user_id=id, club_id=club.id, user_type_id=3)
                    # Establecer la relación bidireccional
                    db.session.add(new_user_interprise)
                    # Agregar los objetos a la sesión
                    db.session.flush()
                    # Confirmar los cambios en la sesión

                db_session.add(new_user)
                db_session.commit()


        except CustomException as ex:
            print(str(ex))
            return CustomException(ex) 

    @classmethod
    def create_user_central(cls, cellphone, user, name, lastname):
        try:
            new_user = UsersCentral(cellphone=cellphone, user=user, name=name, lastname=lastname)
            db.session.add(new_user)
            db.session.flush()
            return new_user
        except CustomException as ex:
            print(str(ex))
            return CustomException(ex) 

    @classmethod
    def save_customer(cls, service_code, user, name, lastname,cellphone, ):
        try:
            wallet_balance = 0.0
            user_central : Union[UsersCentral, Any] = UsersCentral.query.filter_by(cellphone=cellphone).first()
            if user_central is None:
                customer = cls.create_user_central(cellphone, user, name, lastname)
                cls.create_user_in_club( service_code, wallet_balance, customer.id)
                db.session.commit()
                if customer:
                    return customer.as_dict()
                else: return {}
            id = user_central.id
            cls.create_user_in_club(service_code, wallet_balance, id)
            db.session.commit()
            return user_central.as_dict()
        except CustomException as ex:
            print(str(ex))
            return CustomException(ex) 
