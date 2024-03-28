from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException # Errors
from src.utils.Security import Security # Security
from src.services.ModuleMenuService import ModuleMenuService# Groups

main = Blueprint('ModuleMenu_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_module_menus():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            payload = Security.get_payload_token(request.headers)
            user_system_central = payload.get("is_user_system_central")
            service_code = payload.get("service_code")
            items = ModuleMenuService.get_module_menus(user_system_central, service_code)
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
def get_model_menu(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            items = ModuleMenuService.get_model_menu(id)
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

@main.route('/by_profile/<int:profile_id>', methods=['GET'], strict_slashes=False)
def get_menus_by_profile_permissions(profile_id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")
        user_system_central = payload.get("is_user_system_central")

        if user_system_central: #Means that the user is a bdcentral user_system.
            user_system_id = payload.get("user_id")
        else:
            user_system_id = None #Means that the user is a bdgp user_system.

        allowed_menus = ModuleMenuService.get_menus_by_profile_permissions(profile_id, service_code, user_system_id)
        return jsonify({'data': allowed_menus, 'success': True})
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})