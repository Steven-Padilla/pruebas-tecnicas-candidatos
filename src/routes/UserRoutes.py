import json
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from src.services.SignUpService import SignUpService
from src.services.UserService import UserService
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingDataException # Errors
from src.utils.Security import Security # Security
from orm_models import UserToken, Users, UsersCentral
from src.database.db import get_connection_servicecode_orm
from sqlalchemy.orm import scoped_session, sessionmaker
from extensions import db

main = Blueprint('user_profile_blueprint', __name__)

@main.route('/update_firebase_token', methods=['POST'], strict_slashes=False)
def update_firebase_token():
    #has_access = Security.verify_token(request.headers)
    has_access = True
    if has_access:
        try:
            user_id = request.json['user_id']
            firebase_token = request.json['firebase_token']
            #nuevos campos
            uuid = request.json['uuid']
            device = request.json['device']

            user = UsersCentral.query.get(user_id)
            if user:
                token = UserToken.query.filter_by(user_id = user_id, device = device).first()
                
                if token is None:
                    new_token = UserToken(user_id = user_id, token = firebase_token, device = device, uuid = uuid, updated_at = func.now())
                    db.session.add(new_token)    
                else:
                    token.token = firebase_token
                    token.uuid = uuid
                    token.updated_at = func.now()
                db.session.commit()
                data = UserToken.query.filter_by(user_id = user.id).first()
                if data is None:
                    raise(Exception)
                
                return jsonify({'data': data.as_dict() ,'message': 'Firebase token updated successfully', 'success': True})
            else:
            
                return jsonify({'message': 'User not found', 'success': False}), 404
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    
@main.route('/delete_firebase_token', methods=['POST'], strict_slashes=False)
def delete_firebase_token():
    #has_access = Security.verify_token(request.headers)
    has_access = True
    if has_access:
        try:
            user_id = request.json['user_id']
            #nuevos campos
            uuid = request.json['uuid']
            device = request.json['device']

            user = UsersCentral.query.get(user_id)
            if user:
                token = UserToken.query.filter_by(user_id = user_id, device = device, uuid=uuid).first()
                if token is None:
                    return jsonify({'message': 'Firebase token not found', 'success': False}),404
                else:
                    token_json = token.as_dict()
                    db.session.delete(token)
                    db.session.commit()
                return jsonify({'data': token_json ,'message': 'Firebase token deleted successfully', 'success': True})
            else:
                return jsonify({'message': 'User not found', 'success': False}), 404
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    
@main.route('/update/<int:user_id>', methods=['POST'], strict_slashes=False)
def update_user(user_id):
    try:

        body = request.json

        name = body.get('name',None)
        lastname = body.get('lastname',None)
        secondsurname = body.get('secondsurname',None)
        birthday = body.get('birthday',None)
        sex = body.get('sex',None)
        alias = body.get('alias',None)
        
        response = UserService.update(user_id, name, lastname, secondsurname, birthday, sex, alias)

        return response
    except MissingDataException as ex:
        return jsonify({'message': "User not found", 'success': False}), 404
    except DataTypeException as ex:
        print(f'Error: {ex.message}')
        return jsonify({'message': f"Error: {ex.message}", 'success': False}),400
    except Exception as ex:
        print(ex)
        return jsonify({'message': f"ERROR: {ex}", 'success': False}), 400

@main.route('/update/sport/<int:user_id>', methods=['POST'], strict_slashes=False)
def update_sport(user_id):
    try:

        body = request.json
        sport_id = body.get('sport_id', None)
        level_id = body.get('level_id', None)
        
        response = SignUpService.update_sport(user_id, sport_id, level_id)

        return {"data": response, "success": True}
    except MissingDataException as ex:
        return jsonify({'message': "User not found", 'success': False}), 404
    except DataTypeException as ex:
        print(f'Error: {ex.message}')
        return jsonify({'message': f"Error: {ex.message}", 'success': False}),400
    except Exception as ex:
        print(ex)
        return jsonify({'message': f"ERROR: {ex}", 'success': False}), 400

# route to get wallet_balance in Users Model
@main.route('/wallet_balance', methods=['GET'], strict_slashes=False)
def get_wallet_balance():
    has_access = True
    #has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            user_id = request.args.get('user_id')
            service_code = request.args.get('service_code')
            engine_club = get_connection_servicecode_orm(service_code)
            db_club_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_club))
            user = db_club_session.query(Users).filter_by(id=user_id).first()
            if user:
                return jsonify({'data': user.wallet_balance ,'message': 'Wallet balance found successfully', 'success': True})
            else:
                return jsonify({'data': 0.0,'message': 'User not found', 'success': False}), 200
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': f"Error in get_wallet_balance sc:{service_code} user:{user_id} ", 'success': False}), 200
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401


    
