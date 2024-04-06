from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class WalletModes(db.Model, SerializerMixin): 
    __tablename__ = "monedero_modalidad"

    id = Column("id_monedero_modalidad",Integer, primary_key=True)
    name = Column("nombre",String(50), nullable=False)
    status = Column("estatus", Boolean, nullable=False,default=True)
