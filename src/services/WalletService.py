from flask import Blueprint, request, jsonify
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingDataException, MissingKeyException 
from orm_models import Users, UsersCentral, DigitalWallet
from sqlalchemy.orm import scoped_session, sessionmaker

class WalletService:
    @classmethod
    def get_wallets_by_club(this,service_code):
        try:
            wallets=[]
            #Crear conexion con bd del club
            db_session = this.get_db_session(service_code)

            def getId(user):
                return user.id
            #Obtener todos los usuarios de la bd del club
            items = db_session.query(Users).all()
            ids=list(map(getId,items))

            if not items:
                return jsonify({'data': [], 'success': True})

            #Obtener todos los usuarios de la bdcentral
            users = UsersCentral.query.where(UsersCentral.id.in_(ids) & UsersCentral.status == 1).all()
            if not Users:
                return jsonify({'data': [], 'success': True})

            dict = {}
            dict = {value.id: {'name': f"{value.name} {value.lastname} {value.secondsurname}"}
                for value in users}
            for item in items:
                user = dict.get(item.id,None)
                if (user is not None):        
                    wallets.append({
                        'id': item.id,
                        'name': user['name'],
                        'wallet_balance': item.wallet_balance
                    })
            db_session.close()


            return jsonify({'data': wallets, 'success': True})

        except CustomException as ex:
            print(str(ex))
            return CustomException(ex)
        
    def get_db_session(service_code):
        engine = get_connection_servicecode_orm(service_code)
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    @classmethod
    def get_balance_by_user_id(this, service_code,user_id):
        data=[]
        try: 
            db_session=this.get_db_session(service_code)
            wallet_moves=db_session.query(DigitalWallet).where(DigitalWallet.user_id == user_id).all()
            if not wallet_moves:
                return jsonify({'data': [], 'success': True})

            for wallet in wallet_moves:
                data.append(wallet.to_dict())

            return jsonify({'data': data, 'success': True})
            

            
        except CustomException as ex:
            print(str(ex))
            return CustomException(ex)
        

    @classmethod
    def save_new_balance(this, service_code,amount,mode,move_type,concept,user_id):
        try:
            engine = get_connection_servicecode_orm(service_code)
            db_session=scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            
            user=db_session.query(Users).where(Users.id==user_id).first()
            if user is None:
                raise MissingDataException(Users.__tablename__,engine.url.database,user_id)
            
            previous_balance=user.wallet_balance
            current_balance= previous_balance + amount if move_type == 0 else previous_balance - amount 


            move=DigitalWallet(amount=amount, mode=mode, type=move_type,concept=concept, user_id=user_id, previous_balance=previous_balance, current_balance=current_balance)
            user.wallet_balance=current_balance

            db_session.add(move)
            db_session.commit()
            return jsonify({"data":move.to_dict(), "success":True})
            
        except CustomException as ex:
            print(str(ex))
            return CustomException(ex)  
        finally:
            if db_session:
                db_session.close()