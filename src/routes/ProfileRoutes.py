from flask import Blueprint, jsonify, request
from src.utils.errors.CustomException import CustomException, MissingDataException
from src.utils.Security import Security
from src.services.ProfileService import ProfileService  
from datetime import datetime

main = Blueprint('profile_blueprint', __name__)

@main.route('/all', methods=['GET'], strict_slashes=False)
def get_profiles():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        profiles = ProfileService.get_profiles(service_code, user_system_central)
        
        return jsonify({'data': profiles, 'success': True})
    except Exception as e:
        print(f'ProfileRoutes.py - get_profiles() - Error: {str(e)}')
        return jsonify({'message': "Error", 'success': False})
    

@main.route('/<int:profile_id>', methods=['GET'], strict_slashes=False)
def get_profile_by_id(profile_id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        profile = ProfileService.get_profile_by_id(profile_id, service_code, user_system_central)
        
        return jsonify({'data': profile, 'success': True})
    except Exception as e:
        print(f'ProfileRoutes.py - get_profile_by_id() - Error: {str(e)}')
        return jsonify({'message': "Error", 'success': False})

@main.route('/', methods=['POST'], strict_slashes=False)
def save_new_profile():
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
        status = data.get('status')
        permissions = data.get('permissions', [])

        new_profile = ProfileService.save_new_profile(service_code, name, status, permissions, user_system_central)

        return jsonify({"data": new_profile, "success": True})
    except Exception as e:
        print(f'ProfileRoutes.py - save_new_profile() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/update', methods=['POST'], strict_slashes=False)
def update_profile():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json

        profile_id = data.get('profile_id')
        name = data.get('name')
        status = data.get('status')
        permissions = data.get('permissions', [])

        updated_profile = ProfileService.update_profile(profile_id, service_code, user_system_central, name, status, permissions)

        return jsonify({"data": updated_profile, "success": True})
    except MissingDataException as e:
        print(f'ProfileRoutes.py - update_profile() - Error: {e.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as e:
        print(f'ProfileRoutes.py - update_profile() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/delete', methods=['POST'], strict_slashes=False)
def delete_profile():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        user_system_central = payload.get("is_user_system_central")
        service_code = payload.get("service_code")

        data = request.json
        profile_id = data.get('profile_id')

        response = ProfileService.delete_profile(profile_id, service_code, user_system_central)

        return jsonify(response)
    except Exception as e:
        print(f'ProfileRoutes.py - delete_profile() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
