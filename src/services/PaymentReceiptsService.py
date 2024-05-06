from flask import Blueprint, request, jsonify
from src.database.db import get_connection_servicecode_orm
from src.models import Membership, PaymentDiscountMembership, PaymentReceipt, PaymentReceiptDescription, PaymentDiscount, Discount, Packages, Payment
from src.models.payment_receipt_image import PaymentReceiptImage
from src.utils.errors.CustomException import CustomException, DataTypeException, MissingKeyException 
from src.utils.Security import Security 
from orm_models import Users, UsersCentral
from sqlalchemy.orm import scoped_session, sessionmaker
from extensions import db
import pytz
class PaymentReceiptService():
    @classmethod
    def get_single_receipt(cls,service_code,receipt_id):
        try:
            engine = get_connection_servicecode_orm(service_code)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            receipt=(
                db_session.query(
                    PaymentReceipt,
                    PaymentReceiptDescription, 
                    PaymentDiscount,
                    Discount,
                    PaymentReceiptImage
                    )
                    .where(PaymentReceipt.idnotapago == receipt_id)
                    .join(PaymentReceiptDescription, PaymentReceipt.idnotapago == PaymentReceiptDescription.idnotapago)
                    .outerjoin(PaymentDiscount, PaymentDiscount.idnotapago == PaymentReceiptDescription.idnotapago)
                    .outerjoin(Discount, Discount.iddescuento == PaymentDiscount.iddescuento)
                    .outerjoin(PaymentReceiptImage, PaymentReceiptImage.payment_receipt_id == receipt_id)
                    .all())
            receiptData=[]
            if not receipt:
                raise CustomException("Receipt not found")

            for receiptInfo, description, paymentDiscount,discount,image   in receipt:
                membershipPay=db_session.query(PaymentDiscountMembership).where(PaymentDiscountMembership.id_payment_receipt==receipt_id).first()
                motivoMembresia=""
                if  membershipPay is not None:
                    aux=db_session.query(Membership.title).where(Membership.id_membership == membershipPay.id_membership).first()
                    motivoMembresia=aux[0]
                membershipDiscount=int(membershipPay.amount_to_discount) if membershipPay else None
                receiptData.append({
                    "idNotaPago":receiptInfo.idnotapago,
                    "descripcion":description.descripcion,
                    "fecha":receiptInfo.fecha,
                    "folio":receiptInfo.folio,
                    "fechaFactura":receiptInfo.fechafactura,
                    "folioFactura":receiptInfo.foliofactura,
                    "requiereFactura":receiptInfo.requierefactura,
                    "total":receiptInfo.total,
                    "subTotal":receiptInfo.subtotal,
                    "comision":receiptInfo.comisiontotal,
                    "montoDescuento":0 if not paymentDiscount else float(paymentDiscount.montoadescontar),
                    "imagen": ""if not image else  image.image,
                    "motivoDescuento":"" if not discount else discount.titulo, 
                    "montoMonedero":receiptInfo.montomonedero,
                    "metodoPago":receiptInfo.tipopago,
                    "estatus":receiptInfo.estatus,
                    "motivoMembresia":motivoMembresia,
                    "montoMembresia":membershipDiscount,
                    "monto":description.monto
                })
            finalJson= {key: value for key, value in receiptData[0].items() if key not in ["descripcion", "motivoMembresia", "motivoDescuento","monto"]}
            finalJson.update({"descripcion":[]})
            finalJson.update({"motivoMembresia":[]})
            finalJson.update({"motivoDescuento":[]})
            finalJson.update({"montos":[]})
            for singleReceipt in receiptData:
                if singleReceipt.get("descripcion") not in finalJson.get("descripcion"):
                    finalJson["descripcion"].append(singleReceipt.get("descripcion"))
                if singleReceipt.get("motivoMembresia") not in finalJson.get("motivoMembresia"):
                    finalJson["motivoMembresia"].append(singleReceipt.get("motivoMembresia"))
                if singleReceipt.get("motivoDescuento") not in finalJson.get("motivoDescuento"):
                    finalJson["motivoDescuento"].append(singleReceipt.get("motivoDescuento"))
                if singleReceipt.get("monto") not in finalJson.get("montos"):
                    finalJson["montos"].append(singleReceipt.get("monto"))
            return finalJson
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def get_receipts(cls,service_code):
        try:
            engine = get_connection_servicecode_orm(service_code)
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            recipes=(
                db_session.query(
                PaymentReceipt,
                PaymentReceiptDescription,
            )
                .join(PaymentReceiptDescription, PaymentReceipt.idnotapago == PaymentReceiptDescription.idnotapago)).all() 
            users=UsersCentral.query.all()
            user_names={user.id : f'{user.name} {user.lastname} {user.secondsurname}' for user in users} 
            recipes_dics=[]
            for receipt, description in recipes:
                recipes_dics.append({
                    "idRecibo":receipt.idnotapago,
                    "idUsuario":receipt.idusuario,
                    "nombreUsuario":user_names.get(receipt.idusuario,"Sin nombre"),
                    "folio":receipt.folio,
                    "total":receipt.total,
                    "descripcion":description.descripcion,
                    "fecha":receipt.fecha,
                    "idTipoPago":receipt.idtipopago,
                    "tipoPago":receipt.tipopago,
                    "estatus":receipt.estatus,
                })
            return recipes_dics
        except CustomException as ex:
            raise CustomException(ex)