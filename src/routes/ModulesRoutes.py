# ModuleRoutes.py
from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException
from src.utils.Security import Security
from src.services.ModuleService import ModuleService
from datetime import datetime

main = Blueprint('module_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_modules():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            payload = Security.get_payload_token(request.headers)
            user_system_central = payload.get("is_user_system_central")
            service_code = payload.get("service_code")
            
            modules = ModuleService.get_modules(user_system_central, service_code)
            
            if len(modules) > 0:
                return jsonify({'data': modules, 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

@main.route('/<id>', methods=['GET'], strict_slashes=False)
def get_module(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            module = ModuleService.get_module(id)
            if module:
                return jsonify({'data': module.to_json(), 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401