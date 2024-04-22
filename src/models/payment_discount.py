from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from extensions import db

class PaymentDiscount(db.Model, SerializerMixin):
    __tablename__ = 'pagodescuento'

    idpagodescuento = Column(Integer, primary_key=True)
    iddescuento = Column(Integer)
    montopago = Column(String(45))
    montoadescontar = Column(String(45))
    tipo = Column(String(45))
    monto = Column(String(45))
    idpago = Column(ForeignKey('pagos.idpago'), nullable=False, index=True)
    fechacreacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    infodescuento = Column(String)
    idnotapago = Column(ForeignKey('notapago.idnotapago'), nullable=False, index=True)

    notapago = relationship('PaymentReceipt')
    pagos = relationship('Payment')