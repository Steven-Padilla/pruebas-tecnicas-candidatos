from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from extensions import db

class NotapagoComprobante(db.Model, SerializerMixin):
    __tablename__ = 'notapago_comprobante'

    idnotapago_comprobante = Column(Integer, primary_key=True)
    rutacomprobante = Column(String(255))
    fecha = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    estatus = Column(Integer, server_default=text("'0'"))
    idnotapago = Column(ForeignKey('notapago.idnotapago'), nullable=False, index=True)
    comentario = Column(String(255))

    notapago = relationship('PaymentReceipt')