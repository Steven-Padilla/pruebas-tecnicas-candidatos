from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, Text
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Tipodepago(db.Model, SerializerMixin):
    __tablename__ = "tipodepago"

    idtipodepago = Column(Integer, primary_key=True)
    tipo = Column(String(250))
    estatus = Column(Integer, server_default='1')
    habilitarfoto = Column(String(255), server_default='0')
    clavepublica = Column(String(255))
    claveprivada = Column(String(255))
    constripe = Column(Integer, server_default='0')
    cuenta = Column(Text)
    habilitarcampomonto = Column(Integer, comment='0-deshabilitado,1-habilitado')
    habilitarcampomontofactura = Column(Integer, server_default='0', comment='0-deshabilitado,1-habilitado')
    comisionporcentaje = Column(Float(10), server_default='0.00')
    comisionmonto = Column(Float(10), server_default='0.00')
    comisionserviciomonto = Column(Float(10), server_default='0.00')
    comisionservicioporcentaje = Column(Float(10), server_default='0.00')
    impuesto = Column(Float(10))
    habilitarapp = Column(Integer, server_default='0')
    habilitarweb = Column(Integer, server_default='0')
    comisionpornota = Column(Float(10), server_default='0.00')
    tipocomisionpornota = Column(Integer, server_default='0', comment='1.-monto\\n2.-porcentaje')
    factura = Column(Integer, server_default='0')
    habilitartiposervicio = Column(Integer, server_default='0')
    descripciontipopago = Column(String(255))
    habilitarsinrevision = Column(Integer)
    habilitarcatalogo = Column(Integer)
    habilitarcampodigitos = Column(Integer)
    habilitaropciontarjeta = Column(Integer)