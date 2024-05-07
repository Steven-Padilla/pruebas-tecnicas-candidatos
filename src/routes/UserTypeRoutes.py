from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException, MissingDataException # Errors
from src.utils.Security import Security # Security
from src.services.UserTypeService import UserTypeService# Groups

main = Blueprint('UserType_blueprint', __name__)

@main.route('/all', methods=['GET'], strict_slashes=False)
def get_user_types():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        items = UserTypeService.get_user_types(service_code, user_system_central)

        return jsonify({'data': items, 'success': True})    
    except Exception as e:
        print(f'UserTypeRoutes.py - get_user_types() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_type(id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        item = UserTypeService.get_user_type(id, service_code, user_system_central)
        
        return jsonify({'data': item, 'success': True})
    except Exception as e:
        print(f'UserTypeRoutes.py - get_user_type() - Error: {str(e)}')
        return jsonify({'message': "Error", 'success': False})

@main.route('/', methods=['POST'], strict_slashes=False)
def save_user_type():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        access_system = data.get('access_system')
        default = data.get('default')
        is_costumer = data.get('is_costumer')
        name = data.get('name')
        show_on_app = data.get('show_on_app', 0) #default value
        status = data.get('status')

        new_user_type = UserTypeService.save_user_type(service_code, name, show_on_app, status, default, access_system, is_costumer, user_system_central)

        return jsonify({"data": new_user_type, "success": True})
    except Exception as e:
        print(f'UserTypeRoutes.py - save_user_type() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/update', methods=['POST'], strict_slashes=False)
def update_user_type():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        access_system = data.get('access_system')
        default = data.get('default')
        is_costumer = data.get('is_costumer')
        name = data.get('name')
        show_on_app = data.get('show_on_app')
        status = data.get('status')
        user_type_id = data.get('user_type_id')

        updated_user_type = UserTypeService.update_user_type(user_type_id, service_code, user_system_central, name, show_on_app, status, default, access_system, is_costumer)

        return jsonify({"data": updated_user_type, "success": True})
    except MissingDataException as e:
        print(f'UserTypeRoutes.py - update_user_type() - Error: {e.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as e:
        print(f'UserTypeRoutes.py - update_user_type() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/delete', methods=['POST'], strict_slashes=False)
def delete_user_type():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json
        user_type_id = data.get('user_type_id')

        response = UserTypeService.delete_user_type(user_type_id, service_code, user_system_central)

        return jsonify(response)
    except Exception as e:
        print(f'UserTypeRoutes.py - delete_user_type() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})