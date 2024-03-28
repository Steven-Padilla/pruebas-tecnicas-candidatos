from flask import Blueprint, request, jsonify
# from src.database.db import get_connection_servicecode_orm
from src.services.WalletService import WalletService
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingDataException, MissingKeyException 
from src.utils.Security import Security 
from orm_models import Users, UsersCentral, DigitalWallet
# from sqlalchemy.orm import scoped_session, sessionmaker


main = Blueprint('wallet_blueprint', __name__)

@main.route('/', methods=['GET'], strict_slashes=False)
def get_wallets_by_club():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try: 
        service_code = request.args['service_code']
        if not service_code:
            raise MissingKeyException(missing_key="service_code")
            
        response=WalletService.get_wallets_by_club(service_code)
        return response
    
    except MissingKeyException as ex:
        print(f'WalletRoutes.py - get_wallets_by_club() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except CustomException as ex:
            print(str(ex))
            return CustomException(ex)
   
@main.route('/balance/', methods=['GET'], strict_slashes=False)
def get_balance_by_user_id():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        args=request.args
        required_keys=['service_code','user_id']
        for key in required_keys:
            if args.get(key) is None:
                raise MissingKeyException(missing_key=key)
            
        service_code = args['service_code']
        user_id = args['user_id']
        response=WalletService.get_balance_by_user_id(service_code,user_id)


        return response
    
    except MissingKeyException as ex:
        print(f'WalletRoutes.py - get_balance_by_user_id() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)
    
@main.route('/save', methods=['POST'], strict_slashes=False)
def save_new_wallet_move():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        body= request.json
        required_keys=["service_code","amount","mode","type","concept","user_id"]
        for key in required_keys:
            if body.get(key) is None:
                raise MissingKeyException(missing_key=key)

        service_code=body["service_code"]
        amount=body["amount"]
        mode=body["mode"]
        move_type=body["type"]
        concept=body["concept"]
        user_id=body["user_id"]
        response =WalletService.save_new_balance( service_code,amount,mode,move_type,concept,user_id)
        return response
      
    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)
    except MissingDataException as ex:
        print(f'WalletRoutes.py - save_new_wallet_move() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except MissingKeyException as ex:
        print(f'WalletRoutes.py - save_new_wallet_move() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})