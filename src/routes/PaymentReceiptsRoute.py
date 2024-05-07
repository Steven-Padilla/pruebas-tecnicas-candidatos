from flask import Blueprint, request, jsonify
from src.database.db import get_connection_servicecode_orm
from src.models import Membership, PaymentDiscountMembership, PaymentReceipt, PaymentReceiptDescription, PaymentDiscount, Discount, Packages, Payment
from src.models.payment_receipt_image import PaymentReceiptImage
from src.services.PaymentReceiptsService import PaymentReceiptService
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingKeyException 
from src.utils.Security import Security 
from orm_models import Users, UsersCentral
from sqlalchemy.orm import scoped_session, sessionmaker
from extensions import db
import pytz

main = Blueprint('Receipts_blueprint', __name__)

@main.route('/getSingle', methods=['GET'], strict_slashes=False)
def get_single_receipts_v2():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401
    
    try:
        args=request.args
        required_keys=['service_code','receipt_id']
        for key in required_keys:
            if args.get(key) is None:
                raise MissingKeyException(missing_key=key)

        receipt_id = request.args['receipt_id']
        service_code = request.args['service_code']
        data=PaymentReceiptService.get_single_receipt_v2(service_code,receipt_id)
        
        return jsonify({'data': data, 'success': True})
    except MissingKeyException as ex:
        print(f'PaymentReceiptRoute.py - get_single_receipts_v2() - Error: {ex.message}')
        return jsonify({'message': f"Ups, algo salió mal: {ex.message}", 'success': False}),404
    except CustomException as ex:
        print(str(ex))
        return jsonify({'message': f"Ups, algo salió mal: {str(ex)}", 'success': False}),400
    

@main.route('/getAll', methods=['GET'], strict_slashes=False)
def get_receipts_v2():
    has_access = Security.verify_token(request.headers)
    if has_access is False:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

    try:
        args = request.args
        if not args.get('service_code'):
            raise MissingKeyException(missing_key='service_code')

        service_code = request.args['service_code']
        
        data=PaymentReceiptService.get_receipts(service_code)
        response = jsonify({'data': data, 'success': True})
        return response
    except MissingKeyException as ex:
        print(f'PaymentReceiptRoute.py - get_receipts_v2() - Error: {ex.message}')
        return jsonify({'message': f"Ups, algo salió mal: {ex.message}", 'success': False}),404
    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)
    


@main.route('/', methods=['POST'], strict_slashes=False)
def get_receipts():
    # has_access = Security.verify_token(request.headers)
    has_access=True
    if has_access:
        try:
            user = []
            service_code = request.json['service_code']
            engine = get_connection_servicecode_orm(service_code)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

            items = (
            db_session.query(
                PaymentReceipt,
                PaymentReceiptDescription,
                Payment,
                PaymentDiscount,
                Discount,
                Packages,
            )
                .join(PaymentReceiptDescription, PaymentReceipt.idnotapago == PaymentReceiptDescription.idnotapago)
                .outerjoin(Payment, PaymentReceiptDescription.idpago == Payment.id)
                .outerjoin(PaymentDiscount, PaymentDiscount.idpago == PaymentReceiptDescription.idpago)
                .outerjoin(Discount, Discount.iddescuento == PaymentDiscount.iddescuento)
                .outerjoin(Packages, Packages.idpaquete == PaymentReceiptDescription.idpaquete)
            ).all()

            memberships = (
                db_session.query(
                    PaymentReceiptDescription.idnotapago,
                    PaymentReceiptDescription.idpago,
                    PaymentReceipt.descuentomembresia,
                    Membership.title
                )
                .filter(PaymentReceiptDescription.idnotapago == PaymentReceipt.idnotapago, PaymentReceipt.descuentomembresia > 0)
                .join(PaymentDiscountMembership, PaymentReceiptDescription.idnotapago == PaymentDiscountMembership.id_payment_receipt)
                .filter(PaymentReceiptDescription.idpago == PaymentDiscountMembership.id_payment )
                .join(Membership, Membership.id_membership == PaymentDiscountMembership.id_membership)
            ).all()
            
            memberships_dict = {idnotapago: {'amount':round(float(descuentomembresia),2), 'description':title}
                for idnotapago,idpago,descuentomembresia,title in memberships}
            
            users = UsersCentral.query.all()
            
            dict = {value.id: {'name': f"{value.name} {value.lastname} {value.secondsurname}"}
                for value in users}
            
            result_dict = {}

            for receipt, description, payment, discount, discount_name, packages in items:
                idnotapago = receipt.idnotapago
                description_value = description.descripcion.strip() if description else None
                
                amount_value = None
                if description:
                    raw_amount = description.monto
                    amount_value = round(float(raw_amount), 2) if raw_amount and raw_amount.replace('.', '').isdigit() else None

                amount = amount_value

                discount_value = round(float(discount.montoadescontar), 2) if discount else None
                discount_name = discount_name.titulo if discount_name else None

                discount_list = [
                    {'amount': discount_value, 'description': discount_name}
                    for discount_value, discount_name in [(discount_value, discount_name) if discount_value is not None and discount_name is not None else (None, None)]
                    if discount_value is not None 
                ]
                
                discount_membership = receipt.descuentomembresia
                membership_discount = memberships_dict.get(idnotapago, None) if discount_membership and discount_membership > 0 else None
                if membership_discount is not None:
                    discount_list.append(membership_discount)

                if idnotapago not in result_dict:
                    result_dict[idnotapago] = []

                result_dict[idnotapago].append({
                    'description': description_value,
                    'amount': amount,
                    'discounts': discount_list
                })

            for item in items:
                fechaaux = item[0].fecha.replace(tzinfo=pytz.utc)
                formatted_date = fechaaux.strftime("%Y-%m-%d %H:%M:%S")
                newUser = dict.get(item[0].idusuario,None)
                
                
                if newUser is not None:
                    user.append({
                        'id': item[0].idnotapago,
                        'user_id':item[0].idusuario,
                        'folio': item[0].folio,
                        'name': newUser['name'],
                        'payments': result_dict[item[0].idnotapago],
                        'date': formatted_date,
                        'payment_type': item[0].tipopago,
                        'total': item[0].total,
                        'status': item[0].estatus,
                        'comision': item[0].comisiontotal,
                        'bill' : item[0].facturanota,
                        'bill_date': item[0].fechafactura,
                        'bill_folio': item[0].foliofactura,
                        'sub_total': item[0].subtotal,
                        'wallet_amount': item[0].montomonedero,
                    })

            db_session.close()

            return jsonify({'data': user, 'success': True})

        except CustomException as ex:
            print(str(ex))
            return CustomException(ex)
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

@main.route('/<int:receipt_id>/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_receipts_by_user_id(receipt_id, user_id):
    # has_access = Security.verify_token(request.headers)
    has_access = True

    if not has_access:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

    try:
        
        service_code_key = 'service_code'
        if service_code_key not in request.args:
            raise MissingKeyException(service_code_key)
        
        if request.args.get(service_code_key).isdigit():
            service_code = int(request.args.get(service_code_key))
        else:
            raise DataTypeException(service_code_key, int)
    
        engine = get_connection_servicecode_orm(service_code)
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        payment_receipts = (
        db_session.query(
            PaymentReceipt,
            PaymentReceiptDescription,
            Payment,
            PaymentDiscount,
            Discount,
            Packages,
        )
            .filter(PaymentReceipt.idnotapago == receipt_id)
            .join(PaymentReceiptDescription, PaymentReceipt.idnotapago == PaymentReceiptDescription.idnotapago)
            .outerjoin(Payment, PaymentReceiptDescription.idpago == Payment.id)
            .outerjoin(PaymentDiscount, PaymentDiscount.idpago == PaymentReceiptDescription.idpago)
            .outerjoin(Discount, Discount.iddescuento == PaymentDiscount.iddescuento)
            .outerjoin(Packages, Packages.idpaquete == PaymentReceiptDescription.idpaquete)
        ).all()
        # user_id=321
        memberships = (
            db_session.query(
                PaymentReceiptDescription.idnotapago,
                PaymentReceiptDescription.idpago,
                PaymentReceipt.descuentomembresia,
                Membership.title
            )
            .filter(PaymentReceiptDescription.idnotapago == PaymentReceipt.idnotapago, PaymentReceipt.descuentomembresia > 0)
            .join(PaymentDiscountMembership, PaymentReceiptDescription.idnotapago == PaymentDiscountMembership.id_payment_receipt)
            .filter(PaymentReceiptDescription.idpago == PaymentDiscountMembership.id_payment )
            .join(Membership, Membership.id_membership == PaymentDiscountMembership.id_membership)
        ).all()
        
        memberships_dict = {idnotapago: {'amount':round(float(descuentomembresia),2), 'description':title, 'id':idpago}
            for idnotapago,idpago,descuentomembresia,title in memberships}
        
        user = UsersCentral.query.get(user_id)
        
        payment_list = {}

        for receipt, description, payment, discount, discount_name, packages in payment_receipts:
            idnotapago = receipt.idnotapago
            description_value = description.descripcion.strip() if description else None
            
            amount_value = None
            if description:
                raw_amount = description.monto
                amount_value = round(float(raw_amount), 2) if raw_amount and raw_amount.replace('.', '').isdigit() else None

            amount = amount_value

            wallet_amount = None
            if description:
                raw_wallet = description.monederousado
                wallet_amount = round(float(raw_wallet), 2) if raw_wallet and raw_wallet.replace('.', '').isdigit() else None

            wallet = wallet_amount
            
            discount_membership = receipt.descuentomembresia

            discount_value = round(float(discount.montoadescontar), 2) if discount else None
            discount_name = discount_name.titulo if discount_name else None
            
            discount_list = [
                {'amount': discount_value, 'description': discount_name, 'id': discount.idpago}
                for discount_value, discount_name in [(discount_value, discount_name) if discount_value is not None and discount_name is not None else (None, None)]
                if discount_value is not None  
            ]
            
            membership_discount = memberships_dict.get(idnotapago, None) if discount_membership and discount_membership > 0 else None
            if membership_discount is not None:
                discount_list.append(membership_discount)

            if idnotapago not in payment_list:
                payment_list[idnotapago] = []

            payment_list[idnotapago].append({
                'user_id': payment.user_id if payment else user_id, #si no existe pago es porque fue un paquete
                'id':payment.id if payment else packages.idpaquete if packages else None,
                'type': payment.type if payment else None, #si no existe pago no se puede saber que tipo de pago fue
                'description': description_value,
                'amount': amount,
                'discounts': discount_list,
                'wallet_amount': wallet
            })

        unique_receipt_ids = set()
        receipts = []

        for item in payment_receipts:
            fechaaux = item[0].fecha.replace(tzinfo=pytz.utc)
            formatted_date = fechaaux.strftime("%Y-%m-%d %H:%M:%S")
            
            if user is not None:
                receipt_id = item[0].idnotapago
                if receipt_id not in unique_receipt_ids:
                    
                    unique_receipt_ids.add(receipt_id)

                    receipts.append({
                        'id': item[0].idnotapago,
                        'folio': item[0].folio,
                        'name': user.fullname(),
                        'user_id': user.id,
                        'payments': payment_list[item[0].idnotapago],
                        'date': formatted_date,
                        'payment_type': item[0].tipopago,
                        'total': item[0].total,
                        'status': item[0].estatus,
                        'comision': item[0].comisiontotal,
                        'service_commission': item[0].commission_service_total,
                        'card_commission': item[0].commission_card_gateway,
                        'sub_total': item[0].subtotal,
                        'wallet_amount': item[0].montomonedero,
                    })
# 
        db_session.close()

        return jsonify({'data': receipts, 'success': True})
    
    except MissingKeyException as ex:
        print(f'Error: {ex.message}')
        response = jsonify({'message': f"Error: {ex.message}", 'success': False})
        return response, 404
    except DataTypeException as ex:
        print(f'Error: {ex.message}')
        response = jsonify({'message': f"Error: {ex.message}", 'success': False})
        return response, 400
    except CustomException as ex:
        print(str(ex))
        return CustomException(ex)
