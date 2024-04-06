from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy_serializer import SerializerMixin
from src.types.custom_blob import CustomBLOB
from sqlalchemy.orm import relationship
from extensions import db

class UsersSystem(db.Model, SerializerMixin): 
    __tablename__ = "usuarios_sistema"

    id = Column("id",Integer, primary_key=True)
    username = Column("username",String(30), nullable=False)
    password = Column("password", CustomBLOB, nullable=False)
    user_type_id = Column("user_type", Integer, ForeignKey('tipousuario.idtipousuario'), index=True)
    profile_id = Column("profile",Integer, ForeignKey('perfiles.idperfiles'), index=True)
    name = Column("name",String(255), nullable=False)
    lastname = Column("paterno",String(255), nullable=False)
    secondsurname = Column("materno",String(255), nullable=False)
    service_code = Column("service_code", Integer, nullable=False)

    user_type = relationship("UserType") 
    profile = relationship("Profile")