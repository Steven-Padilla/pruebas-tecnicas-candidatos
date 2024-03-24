from flask import Blueprint, jsonify, request
from src.utils.errors.CustomException import CustomException
from src.utils.Security import Security
from src.services.ProfileService import ProfileService  
from datetime import datetime

main = Blueprint('profile_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_profiles():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            profiles = ProfileService.get_profiles(service_code)
            if len(profiles) > 0:
                return jsonify({'data': profiles, 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

@main.route('/<id>', methods=['GET'], strict_slashes=False)
def get_profile(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            service_code = request.json['service_code']
            profile = ProfileService.get_profile(id, service_code)
            if profile:
                return jsonify({'data': profile, 'success': True})
            else:
                return jsonify({'data': [], 'success': True})
        except Exception as ex:
            print(str(ex))
            return jsonify({'message': "Error", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
