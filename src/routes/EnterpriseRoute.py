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
    
@main.route('/update', methods=['POST'], strict_slashes=False)
def update_enterprise():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        body = request.json

        name = body.get("name")
        cellphone = body.get("cellphone")
        telephone = body.get("telephone")
        latitude = body.get("latitude")
        longitude = body.get("longitude")
        postal_code = body.get("postal_code")
        country = body.get("country")
        state = body.get("state")
        city = body.get("city")
        settlement = body.get("settlement")
        neighborhood = body.get("neighborhood")
        address = body.get("address")
    
        json_response = EnterpriseService.update_enterprise(service_code=service_code, 
                                                            name=name, cellphone=cellphone, telephone=telephone,
                                                            latitude=latitude, longitude=longitude, postal_code=postal_code, country=country,
                                                            state=state, city=city, settlement=settlement, neighborhood=neighborhood, 
                                                            address=address)
        
        return jsonify({'data': json_response, 'success': True})
    
    except Exception as e:
        print(f'EnterpriseRoute.py - get_all() - Error: {str(e)}')
        return jsonify({'message': f"{str(e)}", 'success': False}) 
    
    