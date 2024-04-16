from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Discount(db.Model, SerializerMixin):
    __tablename__ = 'descuento'

    iddescuento = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    tipo = Column(Integer, comment='0.-porcentaje\\n1.-monto')
    monto = Column(Float(10), server_default=text("'0.00'"))
    convigencia = Column(Integer, server_default=text("'0'"), comment='0.-notiene\\n1.-tiene vigencia')
    estatus = Column(Integer, server_default=text("'0'"), comment='0.-inactivo\\n1.-activo')
    fechacreacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    porcantidadservicio = Column(String(5), server_default=text("'0'"), comment='Por cantidad de servicios')
    portiposervicio = Column(Integer, server_default=text("'0'"), comment='Por tipo de categoría de servicio')
    porservicio = Column(Integer, server_default=text("'0'"), comment='Por servicios')
    porparentesco = Column(Integer, server_default=text("'0'"), comment='Por parentesco')
    parentescos = Column(String(45))
    porniveljerarquico = Column(Integer)
    fechadecaducidad = Column(String(45), comment='Si se escoge bonificación caducidad en días')
    porclientenoasociado = Column(Integer, server_default=text("'0'"))
    dirigidoserviciocliente = Column(Integer, server_default=text("'0'"), comment='Dirigido a\\n0.-servicio\\n1.-cliente')
    acumuladescuento = Column(Integer, server_default=text("'0'"))
    inppadre = Column(Integer, server_default=text("'0'"))
    inphijo = Column(Integer)
    inpnieto = Column(Integer, server_default=text("'0'"))
    modalidaddescuento = Column(Integer, server_default=text("'0'"), comment='0-descuento\\n1-bonificacion\\n')
    txtdiascaducidad = Column(String(45))
    porhorarioservicio = Column(Integer, server_default=text("'0'"))
    cantidadhorariosservicios = Column(String(45))
    cantidaddias = Column(String(45))
    vigencia = Column(String(45), comment='1.-por periodo\\n2.-por dias')
    hasta = Column(String(45))
    txtnumeroservicio = Column(String(45))
    todosclientes = Column(Integer, server_default=text("'0'"))
    porclientedirecto = Column(Integer, server_default=text("'0'"))
    caracteristicaasociador = Column(Integer, server_default=text("'0'"))
    caracteristicasporservicio = Column(Integer, server_default=text("'0'"))
    caracteristicaportiposervicio = Column(Integer, server_default=text("'0'"))

