from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from extensions import db
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, Text, text 

from sqlalchemy.orm import relationship


class UsersCentral(db.Model, SerializerMixin):
    __tablename__ = 'usuarios_central'
    serialize_rules = ('-reservations.reservations',)
    id = db.Column('idusuarios',db.Integer, primary_key=True, comment='0:USUARIOSINTERNOS,1:USUARIOSEXTERNOS')
    profile_id = db.Column('idperfiles',db.Integer, server_default=text("'0'"))
    ranking = db.Column('ranking', db.Float, server_default = "1.000")
    name= db.Column('nombre',db.String(250))
    lastname= db.Column('paterno',db.String(250))
    secondsurname = db.Column('materno',db.String(250))
    phone = db.Column('telefono',db.String(100), server_default=text("'----'"))
    cellphone = db.Column('celular',db.String(100), server_default=text("'----'"))
    email = db.Column('email',db.String(100))
    user = db.Column('usuario',db.String(255))
    password = db.Column('clave',db.String(100))
    type = db.Column('tipo',db.Integer, server_default=text("'1'"), comment='0:SuperUsuario,1:Empleado,2:Administrador,3:Alumno,5:Coach')
    status = db.Column("estatus",db.Integer, server_default=text("'1'"), comment='0:inactivo,1:activo')
    employee_id = db.Column('idempleados',db.Integer, server_default=text("'0'")) #NO
    firebase_token = db.Column('tokenfirebase',db.String(45), comment='\t') #NO
    os = db.Column('so',db.String(45)) #NO
    birthday= db.Column('fechanacimiento',db.String(100))
    created_at = db.Column('fechacreacion',db.TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    token = db.Column('token',db.String(45)) #Token sms
    picture = db.Column('foto',db.Text)
    stripe_customer_id = db.Column('customerid_stripe',db.String(45)) #NO
    stripe_last_card = db.Column('lastcard_stripe',db.String(45)) #SI
    current_version = db.Column('versionactual',db.String(45))#NO
    validate_phone = db.Column('validartelefono',db.Integer) #NO
    block_data = db.Column('bloquearediciondatos',db.Integer) #NO
    sex = db.Column('sexo',db.String(1))
    wallet_balance = db.Column('saldomonedero',db.Float(14), server_default=text("'0.00'"))
    postal_code = db.Column('codigopostal',db.String(45))
    country = db.Column('pais',db.String(45))
    state = db.Column('estado',db.String(45))
    municipality = db.Column('municipio',db.String(45))
    neighborhood = db.Column('colonia', db.String(45))
    settlement_type= db.Column('tipoasentamiento',db.String(45))
    address = db.Column('calle', db.String(45))
    no_int = db.Column('no_int',db.String(45))
    no_ext = db.Column('no_ext',db.String(45))
    ad_viewed = db.Column('anunciovisto',db.Integer, server_default=text("'0'"))
    system = db.Column('sistema',db.String(45))
    alias = db.Column('alias',Text)
    wallet = db.Column('monedero',db.Float(10), server_default=text("'0.00'"))
    level_id = db.Column('idnivel',db.Integer)
    celphone2 = db.Column('celular2',db.String(45))
    membership_popup = db.Column('popupmembresia',db.Integer, server_default=text("'0'"), comment='0.-no visto\\n1.-visto')
    not_cellphone = db.Column('sincel',db.Integer, server_default=text("'0'"))
    backup_cellphone = db.Column('celularrespaldo',db.String(45))
    terms_accepted = db.Column('aceptopolitica',db.Integer, server_default=text("'0'"))
    enable_schedule = db.Column('habilitarhorarios',db.Integer, server_default=text("'1'"))
    coach_type_id = db.Column('idtipocoach',db.Integer, server_default=text("'0'"))
    

    def fullname(self) -> str:
        return self.name + ' ' + self.lastname + ' ' + self.secondsurname
    
    def as_player_dict(self):
        data = {
            "id": self.id,
            "picture": self.picture,
            "name": self.name,
            "lastname": self.lastname,
        }

        data = {key: "" if value is None else value for key, value in data.items()}
        return data
    
    def as_dict(self):
        user_dict = self.to_dict(
            only=('id','name','lastname','username','email','phone','password')
        )

        return user_dict

class DigitalWallet(db.Model, SerializerMixin):
    __tablename__ = 'monedero'
    
    id = Column('idmonedero',Integer, primary_key=True)
    date = Column('fecha',TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    amount = Column('monto',Float(10), server_default=text("'0.00'"))
    mode = Column('modalidad', Integer, comment='0 - PAGO CAJA\\n1 - por devolución\\n2 - por deposito\\n3 - Cancelacion\\n4 - retiro de monedero\\n\\n')
    type = Column('tipo',Integer, comment='0 - ABONO\\n1 - CARGO')
    previous_balance = Column('saldo_ant',Float(10))
    current_balance = Column('saldo_act',Float(10))
    concept = Column('concepto',String(255))
    user_id = Column('idusuarios',ForeignKey('usuarios.idusuarios'), nullable=False, index=True)
    receipt_id= Column('idnota', Integer, server_default=text("'0'"))
    id_detail_receipt = Column('idnotadescripcion',Integer, server_default=text("'0'"))
    
    usuarios = relationship('Users')

class Users(db.Model, SerializerMixin):
    __tablename__ = 'usuarios'
    id = db.Column('idusuarios',db.Integer, primary_key=True)
    wallet_balance = Column('monedero',db.Float(10), server_default=text("'0.00'"))

    def as_dict(self):
        data={
            'id':self.id,
            'wallet_balance':self.wallet_balance,
        }
        data = {key: "" if value is None else value for key, value in data.items()}
        return data