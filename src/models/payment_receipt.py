from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class PaymentReceipt(db.Model, SerializerMixin):
    __tablename__ = 'notapago'
    idnotapago = Column(Integer, primary_key=True) #auto
    idusuario = Column(Integer, nullable=False)#si
    id_invitado = Column('id_invitado', Integer, ForeignKey('invitados.id'), nullable=True)
    fecha = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")) #auto
    subtotal = Column(Float(12)) #sin comisión stripe
    iva = Column(Float(12)) #no #valor en 0 
    commission_service_total =  Column("comision_servicio_total", Float(12), server_default=text("0.00"))
    commission_card_gateway =  Column("comision_pasarela_tarjeta", Float(12), server_default=text("0.00"))
    total = Column(Float(12)) #mismo de subtotal
    comisiontotal = Column(Float(12)) #comisión stripe, impuesto iva cargo
    commission_amount =  Column("comision_monto", Float(12), server_default=text("0.00"))
    commission_percentage =  Column("comision_porcentaje", Float(12), server_default=text("0.00"))
    amount_equivalent_commission_percentage =  Column("monto_equivalente_comision_porcentaje", Float(12), server_default=text("0.00"))
    commission_service_amount =  Column("comision_servicio_monto", Float(12), server_default=text("0.00"))
    commission_service_percentage =  Column("comision_servicio_porcentaje", Float(12), server_default=text("0.00"))
    amount_equivalent_commission_service_percentage =  Column("monto_equivalente_comision_servicio_porcentaje", Float(12), server_default=text("0.00"))
    montomonedero = Column(Float(12), server_default=text("0.00"))#si uso monedero en el pago 
    estatus = Column(Integer, server_default=text("'0'"), comment='0 - pendiente \\n1-aceptado \\n2.- cancelado\\n3.- no procesado')#cuando se crea se pone en 0 si falla stripe se pone en 3 y cancelado 2
    idtipopago = Column(String(45)) #de la tabla tipo de pago
    tipopago = Column(String(100), comment='0 - Efectivo\\\\n1 - tarjeta de credito\\\\n2 - tarjeta de debito\\\\n3 - cheque\\\\n4 - deposito\\\\n5 - transferencia\\\\n6 - credito\\\\n\\\\n7-oxxopay-8-spei')# descripcion del tipo de pago
    confoto = Column(String(45)) #no 0 cuando se sube comprobante
    datostarjeta = Column(String) #visa mastercard
    idpagostripe = Column(Integer) #tabla pagos stripe inserción de los datos que devuelve stripe
    folio = Column(String(255)) #se genera de tabla paginaconfiguracion campo folio #tomas el que esta en la tabla 
    descuento = Column(Float(12))#no #total de cuanto le descontaste
    descuentomembresia = Column(Float(12))#no
    datostarjeta2 = Column(String) # últimos dígitos numero de tarjeta de stripe 
    montovisual = Column(Float(12), server_default=text("0.00")) #no 0 #monto que pone el usuario al pagar efectivo
    cambio = Column(Float(12), server_default=text("'0.00'")) #no #también para efectivo
    descripcionaceptacion = Column(String) #no #valor ""
    comisionpornota = Column(String(45), server_default=text("'0'"), comment='Se toma el valor del tipo de pago elegido')#comision de servicio
    tipocomisionpornota = Column(String(45), server_default=text("'0'"), comment='Es el tipo monto o porcentaje que esta establecido en el tipo de pago') # si es uno monto si es dos porcentaje
    comisionnota = Column(Float(12), server_default=text("'0.00'"), comment='Es el resultado de la comisión extra que se cobra por cada nota , previamente configurado en el tipo de pago') #0 sin factura
    requierefactura = Column(Integer, server_default=text("'0'")) #1 si requiere factura 0 no
    razonsocial = Column(String(255), comment='\t') #no
    rfc = Column(String(255))
    direccion = Column(String(255))
    nointerior = Column(String(45))
    noexterior = Column(String(45))
    colonia = Column(String(255))
    municipio = Column(String(255))
    estado = Column(String(255))
    codigopostal = Column(String(45))
    correo = Column(String(45))
    pais = Column(String(45))
    asentamiento = Column(String(255))
    calle = Column(String(255))
    formapago = Column(String(45))
    metodopago = Column(String(45))
    usocfdi = Column(String(45))
    imagenconstancia = Column(String)
    idusuariodatofiscal = Column(Integer, server_default=text("'0'"))  # poner 0
    fechafactura = Column(String)
    facturanota = Column(Integer, server_default=text("'0'"))
    foliofactura = Column(String(425))
    fechaaceptacion = Column(String(255))
    idusuarioaceptacion = Column(Integer, server_default=text("'0'"))  # cuando es efectivo se valida en el back y transferencia
    fechareporte = Column(String(255))  # fecha de validación y nota
    fechacancelacion = Column(String(255))  # fecha de cancelacion
    descripcioncancelacion = Column(String)  # motivo de cancelacion
    canceladonota = Column(Integer, server_default=text("'0'"))  # bandera 0 no cancelado 1 cancelado
    idusuariocancelado = Column(Integer, server_default=text("'0'"))  # usuario que cancelo la nota
    tpv = Column(Integer, server_default=text("'0'"))  # 0 desde app 1 desde back
    idbanco = Column(Integer, server_default=text("'0'"))  # 0 #terminal bancaria
    tipotarjeta = Column(String(255))  # debito o credito
    digitostarjeta = Column(String(255))  # ultimos 4 digitos