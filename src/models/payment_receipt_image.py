from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from extensions import db
class PaymentReceiptImage(db.Model,SerializerMixin):
    __tablename__ = 'notapago_comprobante'

    id = Column("idnotapago_comprobante", Integer, primary_key=True)
    image = Column("rutacomprobante", String(255))
    date = Column("fecha", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column("estatus", Integer, server_default=text("'0'"))
    payment_receipt_id = Column("idnotapago", ForeignKey('notapago.idnotapago'), nullable=False, index=True)
    comment = Column("comentario", String(255))

    payment_receipt = relationship('PaymentReceipt')