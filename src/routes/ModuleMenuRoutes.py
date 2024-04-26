from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException, MissingDataException # Errors
from src.utils.Security import Security # Security
from src.services.ModuleMenuService import ModuleMenuService# Groups

main = Blueprint('ModuleMenu_blueprint', __name__)

@main.route('/', methods=['GET'], strict_slashes=False)
def get_module_menus():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        items = ModuleMenuService.get_module_menus(user_system_central, service_code)
        
        return jsonify({'data': items, 'success': True})
    except Exception as ex:
        print(f'ModuleMenuRoutes.py - get_module_menus - {str(ex)}')
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_model_menu(id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        items = ModuleMenuService.get_module_menu(id, service_code, user_system_central)
        
        return jsonify({'data': items, 'success': True})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Error", 'success': False})

@main.route('/by_profile', methods=['GET'], strict_slashes=False)
def get_menus_by_profile_permissions():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")
        user_system_central = payload.get("is_user_system_central")
        profile_id = payload.get("profile_id")

        allowed_menus = ModuleMenuService.get_menus_by_profile_permissions(profile_id, service_code, user_system_central)
        return jsonify({'data': allowed_menus, 'success': True})
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})

@main.route('/', methods=['POST'], strict_slashes=False)
def save_new_module_menu():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")
        profile_id = payload.get("profile_id")

        data = request.json

        module_id = data.get('module_id')
        name = data.get('menu')
        level = data.get('level')
        status = data.get('status')
        path = data.get('file')
        

        new_module = ModuleMenuService.save_new_module_menu(service_code, module_id, name, status, level, path, user_system_central, profile_id)

        return jsonify({"data": new_module, "success": True})
    except Exception as e:
        print(f'ModulesMenuRoutes.py - save_new_module_menu() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/update', methods=['POST'], strict_slashes=False)
def update_module_menu():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        module_menu_id = data.get('id')
        module_id = data.get('module_id')
        name = data.get('name')
        level = data.get('level')
        status = data.get('status')
        path = data.get('file')

        new_module = ModuleMenuService.update_module_menu(module_menu_id, service_code, user_system_central, module_id, name, status, level, path)

        return jsonify({"data": new_module, "success": True})
    except MissingDataException as e:
        print(f'ModuleMenuRoutes.py - update_profile() - Error: {e.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as e:
        print(f'ModuleMenuRoutes.py - update_module_menu() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/delete', methods=['POST'], strict_slashes=False)
def delete_module_menu():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json
        module_menu_id = data.get('id')

        response = ModuleMenuService.delete_module_menu(module_menu_id, service_code, user_system_central)

        return jsonify(response)
    except Exception as e:
        print(f'ModuleMenuRoutes.py - delete_module_menu() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/validate_route', methods=['POST'], strict_slashes=False)
def validate_route_name():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json
        route_name = data.get('route')

        response = ModuleMenuService.validate_route_name(route=route_name, service_code=service_code, user_system_central=user_system_central)

        return jsonify({"data": response, "success": True})
    except Exception as e:
        print(f'ModuleMenuRoutes.py - validate_route_name() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})