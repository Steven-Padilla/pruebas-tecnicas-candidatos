from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Amenity(db.Model, SerializerMixin):
    __tablename__ = "amenidad"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nombre", String(45), nullable=False)
    icon = Column("icono", String(45), nullable=True)
    status = Column("estatus", Integer, nullable=False)
    #dentro del club (lista de switches)
    #0 - No la tiene 1 - si la tiene
    #dentro de bdcentral (catalogo)
    #0 - No visible 1 - Visible 2 - Eliminada 