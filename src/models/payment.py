from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'pagos'
    
    id = Column('idpago',Integer, primary_key=True)
    user_id  = Column('idusuarios',Integer, nullable=True)
    guest_id = db.Column('id_invitado', db.Integer, db.ForeignKey('invitados.id'), nullable=True)
    service_id = Column('idservicio',Integer, server_default=text("'0'")) #no
    reservation_id = Column('id_reservacion',Integer, server_default=text("'0'"))
    membership_id = Column('idmembresia',Integer, server_default=text("'0'")) #no
    type  = Column('tipo', Integer, comment='1.-servicio\\n2.-membresia\\n3.-otros\\n4.-reserva')
    amount = Column('monto',Float(12)) #si #monto del pago de la reserva
    status = Column('estatus',Integer, comment='0.-pendiente\\n1.-proceso\\n2.-aceptado\\n3.-cancelado\\n4.-reembolso\\n5.-sin reembolso\\n\\n6.-rechazado')#si
    payment_date = Column('fechapago',String(255))#si
    card  = Column('tarjeta',String(255)) #no
    creation_date = Column('fechacreacion',TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))#auto
    paid  = Column('pagado',Integer, server_default=text("'0'"), comment='0.-no pagado\\n1.-pagado')#pagado o no #bandera de verificación
    validated_by_user = Column('validadoporusuario',Integer, comment='0.-no validado\\n1.- validado')#no #en 0
    card_digits = Column('digitostarjeta',String(45))#no
    payment_type = Column('tipopago',Integer, comment='1.-tarjeta\\n2.-efectivo')#no #tipo de pago
    event_date = Column('fechaevento',String(45))#no
    divided = Column('dividido',Integer, server_default=text("'0'"), comment='0.-no dividido\\n1.- dividido')#dividido 1 si, 0 no
    start_date = Column('fechainicial',String(45))#no
    end_date = Column('fechafinal',String(45))#no
    concept = Column('concepto',String(255))#descripcion del pago
    payment_type_id = Column('idtipopago',String(255))#no
    payment_method = Column('tipodepago',String(255))#no
    discount = Column('descuento',String(45))#no
    receipt_number = Column('folio',String(255))#no
    requires_acceptance = Column('requiereaceptacion',Integer, server_default=text("'0'"))#no #valor en 0
    accept_service_payment = Column('aceptarserviciopago',Integer, server_default=text("'0'"))#no #valor en 0
    acceptance_date = Column('fechaacepta',String(45))#no #valor en 0
    registration_payment = Column('pagoinscripcion',Integer, server_default=text("'0'")) #no #valor en 0
    