from flask import Blueprint, request, jsonify
from sqlalchemy import func
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingDataException # Errors
from typing import Any, Union
from orm_models import Users, UsersCentral
from src.database.db import get_connection_servicecode_orm
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db
from src.utils.errors.CustomException import CustomException, MissingDataException, MissingKeyException 
from src.services.CustomerService import CustomerService
from src.utils.Security import Security 


main = Blueprint('customer_blueprint', __name__)
@main.route('/all', methods=['GET'], strict_slashes=False)
def get_all_users():

    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:

        service_code = request.args['service_code']
        print(service_code)
        if not service_code:
            raise MissingKeyException(missing_key="service_code")
        json_response = CustomerService.get_all_users(service_code)

        return jsonify({'data': json_response, 'success': True})
    
    except MissingKeyException as e: #estos errores son solo para el desarrollador
        print(f'Error: {e.message}')
        return jsonify({'data': {}, 'message': 'Ups, algo salió mal', 'success': False})
    except MissingDataException as e: #estos errores son solo para el desarrollador
        print(f'Error: {e.message}')
        return jsonify({'data': {}, 'message': 'Ups, algo salió mal', 'success': False})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})
    
@main.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(id):

    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:

        service_code = request.args['service_code']
        print(service_code)
        if not service_code:
            raise MissingKeyException(missing_key="service_code")
        
        json_response = CustomerService.get_user_by_id(service_code, id)

        return jsonify({'data': json_response, 'success': True})
    
    except MissingKeyException as e: #estos errores son solo para el desarrollador
        print(f'Error: {e.message}')
        return jsonify({'data': {}, 'message': 'Ups, algo salió mal', 'success': False})
    except MissingDataException as e: #estos errores son solo para el desarrollador
        print(f'Error: {e.message}')
        return jsonify({'data': {}, 'message': 'Ups, algo salió mal', 'success': False})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})
    
@main.route('/update', methods=['POST'], strict_slashes=False)
def update_user():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
            response = jsonify({'message': 'Unauthorized', 'success': False})
            return response, 401
    try:
        body= request.json

        cellphone=body.get("cellphone")
        user= body.get("user")
        name=body.get("name")
        lastname=body.get("lastname")
        user_id=body.get("user_id")
        password=body.get("password")
        sex=body.get("sex")
        email=body.get("email")
        birthday=body.get("birthday")
        secondsurname=body.get("secondsurname")

        json_response = CustomerService.update_user(user,name,lastname,cellphone,user_id, password, sex, email, birthday, secondsurname)
        
        return jsonify({'data': json_response, 'success': True})
    except Exception as ex:
        print(f"Exception: {str(ex)}")
        return jsonify({'message': f"{str(ex)}", 'success': False})
    
@main.route('/validate_cellphone', methods=['GET'], strict_slashes=False)
def get_user_by_cellphone():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:


        required_keys=["service_code","cellphone"]
        for key in required_keys:
            if key is None:
                raise MissingKeyException(missing_key=key)
        cellphone = request.args.get('cellphone')
        service_code = request.args.get('service_code')

        json_response = CustomerService.search_cellphone(service_code,cellphone)
        

        return {"data": json_response, "success": True}, 200
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})
    
@main.route('/save', methods=['POST'], strict_slashes=False)
def register_customer():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:

        body = request.json
        required_keys=["service_code","name","lastname","cellphone","user"]
        for key in required_keys:
            if key is None:
                raise MissingKeyException(missing_key=key)
        service_code=body["service_code"]
        name=body["name"]
        last_name=body["lastname"]
        cellphone=body["cellphone"]
        user=body["user"]

        json_response = CustomerService.save_customer(service_code,user,name,last_name,cellphone,)
        

        return {"data": json_response, "success": True}, 200
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})
    
