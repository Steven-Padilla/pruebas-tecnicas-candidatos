from flask import Blueprint, request, jsonify
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingDataException, MissingKeyException # Errors
from src.utils.Security import Security # Security
from src.services.CourtService import CourtService# Groups


main = Blueprint('court_blueprint', __name__)

@main.route('/all', methods=['GET'], strict_slashes=False)
def get_courts():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
    
        data = request.args
        service_code = data.get('service_code')

        if service_code is None:
            raise MissingKeyException('service_code')
        
        if service_code.isdigit():
            service_code = int(service_code)
        else:
            raise DataTypeException('service_code', int)

        items = CourtService.get_courts(service_code)
        
        return jsonify({'data': items, 'success': True})
    except MissingDataException as ex:
        print(f'CourtRoutes.py - get_courts() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except DataTypeException as ex:
        print(f'CourtRoutes.py - get_courts() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_court(id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get('service_code')

        if service_code is None:
            raise MissingKeyException('service_code')
        
        item = CourtService.get_court(id, service_code)

        return jsonify({'data': item, 'success': True})
    except MissingDataException as ex:
        print(f'CourtRoutes.py - get_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except DataTypeException as ex:
        print(f'CourtRoutes.py - get_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/', methods=['POST'], strict_slashes=False)
def save_court():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        body = request.json
        address = body.get('address','')

        required_keys = ['service_code','name', 'active', 'enable_reservation_app', 'color', 'image', 'sport_id', 'type_id', 'characteristics']
        characteristic_keys = ['size_id', 'characteristic_id']

        for key in required_keys:
            if body.get(key) is None:
                raise MissingKeyException(missing_key=key)
            
        court_caracteristic = body['characteristics']

        for key in characteristic_keys:
            if court_caracteristic.get(key) is None:
                raise MissingKeyException(missing_key=f'characteristics.{key}')

        service_code = body['service_code']
        name = body['name']
        active = body['active']
        enable_reservation_app = body['enable_reservation_app']
        color = body['color']
        image = body['image']

        id_sport = body['sport_id']
        id_court_type = body['type_id']
        id_zone_size = court_caracteristic['size_id']
        id_court_caracteristic = court_caracteristic['characteristic_id']

        if not isinstance(service_code, int):
            raise DataTypeException('service_code', int)
        if not isinstance(active, int):
            raise DataTypeException('active', int)
        if not isinstance(enable_reservation_app, int):
            raise DataTypeException('enable_reservation_app', int)
        if not isinstance(id_zone_size, int):
            raise DataTypeException('size_id', int)
        if not isinstance(id_sport, int):
            raise DataTypeException('sport_id', int)
        if not isinstance(id_court_type, int):
            raise DataTypeException('type_id', int)
        if not isinstance(id_court_caracteristic, int):
            raise DataTypeException('characteristic_id', int)

        new_court = CourtService.save_court(service_code, name,address,active, enable_reservation_app,color,image,id_zone_size,id_sport,id_court_type,id_court_caracteristic)

        return jsonify({'data': new_court, 'success': True})
    except MissingDataException as ex:
        print(f'CourtRoutes.py - save_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except DataTypeException as ex:
        print(f'CourtRoutes.py - save_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Error", 'success': False})
    
@main.route('/update/<int:court_id>', methods=['POST'], strict_slashes=False)
def update_court(court_id):
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        body = request.json

        id_zone_size = None
        id_court_characteristics = None

        address = body.get('address')
        service_code = body.get('service_code')
        name = body.get('name')
        active = body.get('active')
        enable_reservation_app = body.get('enable_reservation_app')
        color = body.get('color')
        image = body.get('image')

        id_sport = body.get('sport_id')
        id_court_type = body.get('type_id')
        court_characteristics = body.get('characteristics')

        if court_characteristics is not None:
            id_court_characteristics = court_characteristics.get('characteristic_id')
            id_zone_size = court_characteristics.get('size_id')
            
        response = CourtService.update_court(court_id, service_code, name, address, active, enable_reservation_app, color, image, id_zone_size, id_sport, id_court_type, id_court_characteristics)
        return jsonify(response)
    except MissingDataException as ex:
        print(f'CourtRoutes.py - update_courts() - Error: {ex.message}')
        return jsonify({'data': {}, 'success': True})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/delete', methods=['POST'], strict_slashes=False)
def delete_court():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        body = request.json
        required_keys = ['service_code','id']

        for key in required_keys:
            if body.get(key) is None:
                raise MissingKeyException(missing_key=key)
            
        court_id = body['id']
        service_code = body['service_code']

        if not isinstance(service_code, int):
            raise DataTypeException('service_code', int)
        if not isinstance(court_id, int):
            raise DataTypeException('id', int)
            
        response = CourtService.delete_court(court_id, service_code)
        return jsonify(response)
    except MissingKeyException as ex:
        print(f'CourtRoutes.py - delete_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except MissingDataException as ex:
        print(f'CourtRoutes.py - delete_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except DataTypeException as ex:
        print(f'CourtRoutes.py - delete_court() - Error: {ex.message}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    except Exception as ex:
        print(str(ex))
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/sports', methods=['GET'], strict_slashes=False)
def get_sports_catalog():
    try:
        data = CourtService.get_sports_catalog()
        return jsonify({'data': data, 'success': True})
    except Exception as e:
        print(f'CourtRoutes.py - get_sports_catalog() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})

@main.route('/types', methods=['GET'], strict_slashes=False)
def get_types_catalog():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        data = CourtService.get_court_type_catalog(service_code)

        return jsonify({'data': data, 'success': True})
    except Exception as e:
        print(f'CourtRoutes.py - get_types_catalog() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False})
    
@main.route('/sizes', methods=['GET'], strict_slashes=False)
def get_sizes_catalog():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        data = CourtService.get_court_size_catalog(service_code)

        return jsonify({'data': data, 'success': True})
    except Exception as e:
        print(f'CourtRoutes.py - get_sizes_catalog() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False}) 

@main.route('/characteristics', methods=['GET'], strict_slashes=False)
def get_characteristic_catalog():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        payload = Security.get_payload_token(request.headers)
        service_code = payload.get("service_code")

        data = CourtService.get_court_characteristic_catalog(service_code)

        return jsonify({'data': data, 'success': True})
    except Exception as e:
        print(f'CourtRoutes.py - get_characteristic_catalog() - Error: {str(e)}')
        return jsonify({'message': "Ups, algo salió mal", 'success': False}) 