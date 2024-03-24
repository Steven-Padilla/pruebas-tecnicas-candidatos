from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException # Errors
from src.utils.Security import Security # Security
from src.services.UserTypeService import UserTypeService# Groups

main = Blueprint('UserType_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_user_types():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            items = UserTypeService.get_user_types(service_code)
            if (len(items) > 0):
                return jsonify({'data': items, 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    
    
@main.route('/<id>', methods=['GET'], strict_slashes=False)
def get_user_type(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            item = UserTypeService.get_user_type(id, service_code)
            if (item != None):
                return jsonify({'data': item, 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401