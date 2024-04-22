from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from extensions import db

class PaymentReceiptDescription(db.Model, SerializerMixin):
    __tablename__ = "notapago_descripcion"

    idnotapago_descripcion = Column(Integer, primary_key=True)
    idnotapago = Column(ForeignKey('notapago.idnotapago'), nullable=False, index=True)
    descripcion = Column(String(255)) #descripcion del pago
    cantidad = Column(String(45))  #cantidad 1
    monto = Column(String(45)) #monto del pago el mismo
    idpago = Column(Integer) # id pago
    fecha = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")) #auto
    idpaquete = Column(Integer) #no
    costounitario = Column(String(45)) #no 
    monederousado = Column(String(250), server_default=text("'0'")) #si se uso monedero
    
    notapago = relationship('PaymentReceipt')