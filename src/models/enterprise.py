from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Enterprise(db.Model, SerializerMixin):
    __tablename__ = "empresa"

    id = Column("idempresa", Integer, primary_key=True, autoincrement=True)
    name = Column("nombre", String(255))
    telephone = Column("telefono", String(45))
    cellphone = Column("celular", String(100))
    latitude = Column("latitud", String(255))
    longitude = Column("longitud", String(255))
    postal_code = Column("codigopostal", String(45))
    country = Column("pais", String(45))
    state = Column("estado", String(45, collation="utf8mb3_general_ci"))
    city = Column("municipio", String(45, collation="utf8mb3_general_ci"))
    settlement = Column("asentamiento", String(45))
    neighborhood = Column("colonia", String(45, collation="utf8mb3_general_ci"))
    address = Column("direccion", String(45, collation="utf8mb3_general_ci"))
    status = Column("estatus", Integer)
    service_code = Column("codserv", Integer)
    image = Column("imagen", String(255))
    reserve_day_limit = Column("limitediasreserva", Integer)