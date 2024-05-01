from flask import Blueprint, jsonify, request
from src.utils.Security import Security
from ..services.ScheduleService import ScheduleService
    
main = Blueprint('schedule_blueprint', __name__)

@main.route('/', methods=['GET'], strict_slashes=False)
def get_schedule():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        data = ScheduleService.get_schedule(service_code=service_code)

        return jsonify({"data": data, "success": True})
    
    except Exception as e:
        print(f'ScheduleRoute.py - get_schedule() - Error: {str(e)}')
        return jsonify({'message': f"{str(e)}", 'success': False}) 
    
@main.route('/update', methods=['POST'], strict_slashes=False)
def update_schedule():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        body = request.json
    
        json_response = ScheduleService.update_schedule(**body)
        
        return jsonify({'data': json_response, 'success': True})
    
    except Exception as e:
        print(f'ScheduleRoute.py - update_schedule() - Error: {str(e)}')
        return jsonify({'message': f"{str(e)}", 'success': False}) 
    
    