from flask import Blueprint, request, jsonify
# from src.database.db import get_connection_servicecode_orm
from src.services.WalletService import WalletService
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingKeyException 
from src.utils.Security import Security 
from orm_models import Users, UsersCentral, DigitalWallet
# from sqlalchemy.orm import scoped_session, sessionmaker


main = Blueprint('wallet_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_wallets_by_club():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try: 
        service_code = request.json['service_code']
        response=WalletService.get_wallets_by_club(service_code)
        return response
    except CustomException as ex:
            print(str(ex))
            return CustomException(ex)
    

@main.route('/balance/', methods=['POST'], strict_slashes=False)
def get_balance_by_userId():
    try:
        service_code = request.json['service_code']
        user_id = request.json['user_id']
        print(user_id)
        response=WalletService.get_balance_by_user_id(service_code,user_id)
        return response
    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)
"""
TODO: Creación de Módulo "Monedero"
    - Traer registros de monedero por usuario
    - Traer balances actuales de monedero por usuario
    - Guardar movimientos de monedero (Cargo/Abono)
"""