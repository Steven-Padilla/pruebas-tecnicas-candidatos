from typing import Any, Union
from flask import Blueprint, jsonify, request
from orm_models import Users, UsersCentral
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException, MissingDataException, MissingKeyException
from src.services._ExampleService import ExampleService

main = Blueprint('example_blueprint', __name__)

#Ruta dinámica
@main.route('/<int:param>', methods=['GET'], strict_slashes=False)
def get_example(param):
    try:
        json_response = {'parametro': param}

        return jsonify({'data': json_response, 'success': True})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})
    
#Query parameters
@main.route('/search', methods=['GET'], strict_slashes=False)
def query_parameters_example():
    try:
        query_parameters = request.args

        print(query_parameters) #diccionario de dict[str, str]

        product_id = request.args.get('productId')
        customer_id = request.args.get('customerId') #Si no se incluye el valor por defecto será null

        json_response = {'product_id' : product_id, 'customer_id': customer_id}

        return jsonify({'data': json_response, 'success': True})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})

#body
@main.route('/', methods=['POST'], strict_slashes=False)
def body_example():
    try:
        data = request.data #se obtiene en bytes
        print(data)

        # Si el cuerpo está en formato JSON (diccionario)
        body = request.json
        print(body)

        product_id = body.get('productId') # tambien es accesible como body["productId"]
        customer_id = body.get('customerId')
        # customer_id = body['customerId'] #Si no se incluye en el cuerpo, retornará un error por eso es mejor usar el método get

        json_response = {'product_id' : product_id, 'customer_id': customer_id}

        return jsonify({'data': json_response, 'success': True})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})

#Usando modelos de la bdcentral
@main.route('/model', methods=['GET'], strict_slashes=False)
def model_example():
    try:
        #Se utiliza SQL Alchemy ORM 
        first_user: Union[UsersCentral, Any] = UsersCentral.query.first() #Puedes usar tipado de python 3.9 (no requerido) https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

        #Validar la información (usar "Guard Clauses" o "Early Returns" según se requiera)
        if first_user is None:
            raise CustomException('Usuario no encontrado')

        print(first_user) #Objeto de la clase UsersCentral cada columna se vuelve un atributo

        print(first_user.id)
        print(first_user.name)

        #Los modelos cuentan con un serializer para obtenerlos en formato JSON ()
        json_response = first_user.to_dict(only=('id','name')) #funciones only() y rules() reciben tuplas

        print(first_user.to_dict(rules=('-id',))) #'rules' recibe columnas que no quieres enviar. 'only' hace el caso contrario
        print(first_user.to_dict(only=('name',)))

        return jsonify({'data': json_response, 'success': True})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})

#Usando modelos de la bd de cada club
@main.route('/model/<int:service_code>', methods=['GET'], strict_slashes=False)
def model_club_example(service_code): #puedes probar con 144
    try:
        """
        1. Se requiere el código de servicio siempre que requieras usar la bd del club
        2. La sintaxis cambia un poco pero una vez obtenido los datos es exactamente igual
        3. Un modelo puede estar presente tanto en la estructura de la bdcentral como la bd del club
        4. Todos los modelos que estan en una bd de club, estan en las bd de los demás clubes
        """

        #Obtenemos una "session" que este conectada a la bd del club
        engine = get_connection_servicecode_orm(service_code)
        with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
            db_session: Session

        #Se utiliza SQL Alchemy ORM 
        first_user: Union[Users, Any] = db_session.query(Users).first()

        #Validar la información (usar "Guard Clauses" o "Early Returns" según se requiera)
        if first_user is None:
            raise CustomException('Usuario no encontrado')

        print(first_user) #Objeto de la clase Users cada columna se vuelve un atributo

        print(first_user.id)
        print(first_user.wallet_balance)

        json_response = first_user.to_dict(only=('id',))

        print(first_user.to_dict())

        return jsonify({'data': json_response, 'success': True})
    except CustomException as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': f'Error: {str(e)}', 'success': False})

#Usando funciones de la clase ExampleService
@main.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def user_example(user_id):
    try:
        """
        El routes sirve para recibir los datos de las peticiones y validar que esten correctos antes de hacer
        las queries a la bd, algunas validaciones que deben hacerse siempre son:

        - Tipo de dato (datos válidos)
        - Los datos requeridos deben venir en la request

        despues se usa el archivo Service correspondiente para todo el manejo de la información
        """

        service_code = request.args.get('service_code')
        if service_code is None:
            raise MissingKeyException('service_code')
        
        service_code = int(service_code)
        
        json_response = ExampleService.get_user_data_with_wallet_amount(user_id, service_code)

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