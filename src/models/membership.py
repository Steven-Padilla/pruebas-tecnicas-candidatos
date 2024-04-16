from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, text
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Membership(db.Model, SerializerMixin):
    __tablename__ = 'membresia'

    id_membership = Column('idmembresia',Integer, primary_key=True)
    title = Column('titulo', String(255))
    subtitle = Column('subtitulo', String(255))
    image = Column('imagen', String(255))
    cost = Column('costo', Float(12))
    status = Column('estatus', Integer, server_default=text("'0'"))
    order = Column('orden', Integer, server_default=text("'0'"))
    creation_date = Column('fechacreacion', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    duration_in_days = Column('cantidaddias', String(255), comment='Unidad mínima que se debe configurar para saber la duración en que va durar la membresía')
    payment_time = Column('tiempodepago', String(45), comment='Es el tiempo que se le da para el usuario que tenga la membresía lo pueda pagar')
    description = Column('descripcion', String)
    per_day = Column('pordia', Integer, server_default=text("'0'"))
    per_month = Column('pormes', Integer, server_default=text("'0'"))
    per_year = Column('poranio', Integer, server_default=text("'0'"))
    number_of_days = Column('numerodia', String(45))
    starting_from_date = Column('apartirdefecha', String(255))
    per_category = Column('porcategoria', Integer, server_default=text("'0'"))
    per_service = Column('porservicio', Integer, server_default=text("'0'"))
    color = Column('color', String(100))
    depends = Column('depende', Integer, server_default=text("'0'"), comment='0.-no depende\\n1.-depende')
    id_membership_depends_on = Column('idmembresiadepende', Integer, server_default=text("'0'"))
    input_parent = Column('inppadre', Integer, server_default=text("'0'"))
    input_child = Column('inphijo', Integer, server_default=text("'0'"))
    input_grandchild = Column('inpnieto', Integer, server_default=text("'0'"))
    limit = Column('limite', String(45), server_default=text("'0'"))
    date = Column('fecha', String(45))
    repeat = Column('repetir', Integer, server_default=text("'0'"))
    per_schedule = Column('porhorario', Integer, server_default=text("'0'"))
    discount_type_per_schedule = Column('tipodescuentoporhorario', String(45))
    amount_per_schedule = Column('montoporhorario', String(45))
    enrollment_cost = Column('costoinscripcion', Float(12), server_default=text("'0.00'"))
    enable_wallet = Column('habilitarmonedero', Integer, server_default=text("'0'"))
