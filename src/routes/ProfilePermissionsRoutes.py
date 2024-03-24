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

@main.route('/<profile_id>/getpermission', methods=['POST'], strict_slashes=False)
def get_permission(profile_id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            id_permission = request.json['id']
            permission = ProfilePermissionsService.get_permission(id_permission, service_code, profile_id)
            return jsonify({'data': permission, 'success': True})
            
        except CustomException as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        return jsonify({'message': 'Unauthorized', 'success': False})
