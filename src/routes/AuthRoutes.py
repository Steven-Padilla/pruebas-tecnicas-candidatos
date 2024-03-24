from flask import Blueprint, request, jsonify
from jwt import ExpiredSignatureError
from src.utils.Security import Security # Security
from src.services.AuthService import AuthService # Services

from src.utils.errors.CustomException import MissingDataException

main = Blueprint('auth_blueprint', __name__)

@main.route('/', methods=['POST'],strict_slashes=False)
def login():
    try:
        service_code=request.json['service_code']
        username = request.json['username']
        password = request.json['password']
    
        response = AuthService.login_user(username, password, service_code)

        return jsonify(response)
        
    except MissingDataException as ex:
        print(f'AuthRoutes.py - login() - Error: {ex.message}')
        return jsonify({'message': 'Datos de inicio de sesión incorrectos', 'success': False})
    except Exception as ex:
        print(f'AuthRoutes.py - login() - Error: {str(ex)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/verify_token', methods=['POST'],strict_slashes=False)
def verify():
    try:
        token = request.json['token']

        payload = Security.decode_token(token)
        print(payload)
        is_expired = Security.validate_exp(payload)
        print(is_expired)
        if is_expired:
            response = jsonify({'message': 'Datos de inicio de sesión incorrectos', 'success': False})
            return response, 401
        return jsonify({'success': True})
    except ExpiredSignatureError:
        response = jsonify({'message': 'Datos de inicio de sesión incorrectos', 'success': False})
        return response, 401    
    except Exception as ex:
        print(f'AuthRoutes.py - verify() - Error: {str(ex)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/renew', methods=['POST'],strict_slashes=False)
def renew():
    try: 
        encoded_token = Security.renew_token(request.headers)
        if (encoded_token != None):
            return jsonify({'token': encoded_token, 'success': True})
        else:
            response = jsonify({'message': 'Unauthorized' , 'success': False})
            return response, 401
    except Exception as ex:
        print(f'AuthRoutes.py - renew() - Error: {str(ex)}')
        return jsonify({'message': "ERROR", 'success': False})
    