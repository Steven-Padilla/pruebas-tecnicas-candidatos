from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException
from src.utils.Security import Security
from src.services.ProfilePermissionsService import ProfilePermissionsService

main = Blueprint('profile_permissions_blueprint', __name__)

@main.route('/<profile_id>/permissions', methods=['POST'], strict_slashes=False)
def get_permissions(profile_id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            permissions = ProfilePermissionsService.get_permissions(profile_id, service_code)
            return jsonify({'data': [permission.to_json() for permission in permissions], 'success': True})
            
        except CustomException as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

@main.route('/submodule', methods=['GET'], strict_slashes=False)
def get_permission_module_by_profile_id():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            data = request.args
            payload = Security.get_payload_token(request.headers)

            

            service_code = payload.get("service_code")
            is_user_system_central = payload.get("is_user_system_central")
            submodule_id = data['submodule_id']
            profile_id = data['profile_id']

            if submodule_id.isdigit():
                submodule_id = int(submodule_id)

            if profile_id.isdigit():
                profile_id = int(profile_id)

            permission = ProfilePermissionsService.get_permission_module_by_profile_id(submodule_id, profile_id, service_code, is_user_system_central)
            return jsonify({'data': permission, 'success': True})
            
        except CustomException as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        return jsonify({'message': 'Unauthorized', 'success': False})
