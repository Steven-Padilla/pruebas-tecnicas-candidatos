# ModuleRoutes.py
from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException, MissingDataException
from src.utils.Security import Security
from src.services.ModuleService import ModuleService
from datetime import datetime

main = Blueprint('module_blueprint', __name__)

@main.route('/', methods=['GET'], strict_slashes=False)
def get_modules():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        modules = ModuleService.get_modules(user_system_central, service_code)

        return jsonify({'data': modules, 'success': True})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Error", 'success': False})

@main.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_module(id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        module = ModuleService.get_module(id, service_code, user_system_central)
        
        return jsonify({'data': module, 'success': True})
    except Exception as e:
        print(f'ModulesRoutes.py - get_module() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/', methods=['POST'], strict_slashes=False)
def save_new_module():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        name = data.get('name')
        level = data.get('level')
        status = data.get('status')
        icon = data.get('icon')

        new_module = ModuleService.save_new_module(service_code, name, status, level, icon, user_system_central)

        return jsonify({"data": new_module, "success": True})
    except Exception as e:
        print(f'ModulesRoutes.py - save_new_module() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/update', methods=['POST'], strict_slashes=False)
def update_module():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        module_id = data.get('module_id')
        name = data.get('name')
        level = data.get('level')
        status = data.get('status')
        icon = data.get('icon')

        new_module = ModuleService.update_module(module_id, service_code, user_system_central, name, status, level, icon)

        return jsonify({"data": new_module, "success": True})
    except MissingDataException as e:
        print(f'ModulesRoutes.py - update_profile() - Error: {e.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as e:
        print(f'ModulesRoutes.py - update_module() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/delete', methods=['POST'], strict_slashes=False)
def delete_module():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json
        module_id = data.get('module_id')

        response = ModuleService.delete_module(module_id, service_code, user_system_central)

        return jsonify(response)
    except Exception as e:
        print(f'ModulesRoutes.py - delete_module() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})