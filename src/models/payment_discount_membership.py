from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from extensions import db

class PaymentDiscountMembership(db.Model, SerializerMixin):
    __tablename__ = 'pagodescuentomembresia'

    id_payment_discount_membership = Column('idpagodescuentomembresia',Integer, primary_key=True)
    id_payment = Column('idpago', ForeignKey('pagos.idpago'), nullable=False, index=True)
    id_membership = Column('idmembresia',Integer, nullable=False, server_default=text("'0'"))
    id_service = Column('idservicio',Integer)
    discount = Column('descuento',Integer)
    amount = Column('monto',String(255))
    amount_to_discount = Column('montoadescontar',String(255))
    creation_date = Column('fechacreacion', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    id_payment_receipt = Column('idnotapago', ForeignKey('notapago.idnotapago'), nullable=False, index=True)

    payment_receipt = relationship('PaymentReceipt')
    payments = relationship('Payment')