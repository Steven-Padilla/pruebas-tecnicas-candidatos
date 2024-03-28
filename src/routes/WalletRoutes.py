from flask import Blueprint, request, jsonify
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingKeyException 
from src.utils.Security import Security 
from orm_models import Users, UsersCentral, DigitalWallet
from sqlalchemy.orm import scoped_session, sessionmaker


main = Blueprint('wallet_blueprint', __name__)

@main.route('/', methods=['POST'], strict_slashes=False)
def get_wallets_by_club():
    has_access = Security.verify_token(request.headers)
    if has_access == False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    try:
        wallets=[]
        service_code = request.json['service_code']
        #Crear conexion con bd del club
        engine = get_connection_servicecode_orm(service_code)
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        #Obtener todos los usuarios de la bd del club
        items = db_session.query(Users).all()

        if not items:
            return jsonify({'data': [], 'success': True})
        
        #Obtener todos los usuarios de la bdcentral
        users = UsersCentral.query.filter(UsersCentral.status == 1).all()

        """
        TODO: Optimizar y completar el proceso para obtener el monedero de cada usuario

        - Los datos como nombre, apellidos, foto se almacenan en la bdcentral
        - El monedero es por club, por lo que el saldo solo se encuentra en la bd del club

        Retorno:
            Listado con datos del usuario y saldo del mismo, además de los movimientos de su monedero
        """
        dict = {}
        dict = {value.id: {'name': f"{value.name} {value.lastname} {value.secondsurname}"}
            for value in users}
        for item in items:
            user = dict.get(item.id,None)
            if (user != None):        
                wallets.append({
                    'id': item.id,
                    'name': user['name'],
                    'wallet_balance': item.wallet_balance
                })
        db_session.close()


        return jsonify({'data': wallets, 'success': True})

    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)

"""
TODO: Creación de Módulo "Monedero"
    - Traer registros de monedero por usuario
    - Traer balances actuales de monedero por usuario
    - Guardar movimientos de monedero (Cargo/Abono)
"""