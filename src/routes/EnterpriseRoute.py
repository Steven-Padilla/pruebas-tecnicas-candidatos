from flask import Blueprint, jsonify, request
from src.utils.Security import Security
from ..services.EnterpriseService import EnterpriseService
    
main = Blueprint('enterprise_blueprint', __name__)

@main.route('/', methods=['GET'], strict_slashes=False)
def get_enterprise():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        data = EnterpriseService.get_enterprise_data(service_code=service_code)

        return jsonify({"data": data, "success": True})
    
    except Exception as e:
        print(f'EnterpriseRoute.py - get_all() - Error: {str(e)}')
        return jsonify({'message': f"{str(e)}", 'success': False}) 