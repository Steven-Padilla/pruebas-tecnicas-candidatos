from datetime import datetime
from typing import Any, Union
from sqlalchemy_serializer import SerializerMixin
from extensions import db
from sqlalchemy import CHAR, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, Text, TypeDecorator, cast, func, text, BLOB, type_coerce 
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
            only=('id','name','lastname','user','email','cellphone','password', 'picture', 'ranking', 'alias', 'secondsurname', 'birthday', 'sex')
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

class Courts(db.Model, SerializerMixin):
    __tablename__ = 'zonas'
    serialize_rules = ('-address','-estatus','-color','-configuration_id','-image')
    id = Column('idzona', Integer, primary_key=True)
    name = Column('nombre',String(255))
    address = Column('direccion',String(45))
    active = Column('cancha_activa',Integer, server_default="1", comment='0.-inactivo\t\\n1.-activo\t\\n2.-Eliminada')
    enable_reservation_app = Column('habilitar_reservas_app',Integer, comment='0.-inactivo\t\\n1.-activo')
    color = Column('color',String(45))
    configuration_id = Column('idzonasconfiguracion',ForeignKey('zonasconfiguracion.idzonasconfiguracion'), index=True, server_default=text("'0'"))
    image = Column('imagen',String(255))
    size_id = Column('tamanio_cancha', ForeignKey('tamanio_cancha.id'),index=True)
    sport = Column('deporte', Integer,index=True)
    type_id = Column('tipo_cancha',ForeignKey('tipo_cancha.id'),index=True)
    characteristic_id = Column('caracteristica_cancha',ForeignKey('caracteristica_cancha.id'),index=True)
    
    characteristic = relationship('CourtCharacteristic')
    type = relationship('CourtType')
    size = relationship('CourtSize')
    configuration = relationship('CourtsConfiguration')
    
    ##only specific colums
    def to_dict_for_app_choose_court_list(self):
        court_colums = ("id", "name", "image")
        characteristic_columns = ("characteristic.caracteristic",)
        size_columns = ("size.size",)
        type_columns = ("type.type",)

        reservation_dict = self.to_dict(
            only=court_colums + characteristic_columns + size_columns + type_columns
        )
        return reservation_dict
    def to_json(self, sport_name: str) -> dict[str, Any]:
        """
            Generates the json that uses the gp_admin model

            Params:
                sport_name: Name of the sport object obtained from bdcentralgp
        """
        court_colums = ("id","name","active","color","image","type_id", "enable_reservation_app")
        characteristics = self.characteristic
        size = self.size
        court_type = self.type
        court_dict: Union[dict, Any] = self.to_dict(only=court_colums)
        court_dict.update({"sport":sport_name, "sport_id": self.sport, "type":court_type.type, "characteristics": {"characteristic" : characteristics.caracteristic, "characteristic_id" : characteristics.id, "size":size.size, "size_id":size.id}})
        
        return court_dict

class CourtCharacteristic(db.Model, SerializerMixin):
    __tablename__ = "caracteristica_cancha"

    id = Column(Integer, primary_key=True)
    caracteristic = Column(String(45, collation="utf8mb3_unicode_ci"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP")

class CourtType(db.Model, SerializerMixin):
    __tablename__ = "tipo_cancha"

    id = Column(Integer, primary_key=True)
    type = Column(String(45, collation="utf8mb3_unicode_ci"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP")

class CourtSize(db.Model, SerializerMixin):
    __tablename__ = "tamanio_cancha"

    id = Column(Integer, primary_key=True)
    size = Column(String(45, collation="utf8mb3_unicode_ci"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default="CURRENT_TIMESTAMP")

class Sport(db.Model, SerializerMixin):
    __tablename__ = "deporte"

    id = Column("iddeporte", Integer, primary_key=True, autoincrement=True)
    name = Column("deporte", String(255))
    status = Column("estatus", Integer, comment="0.-inactivo\n1.-activo")

class CourtsConfiguration(db.Model, SerializerMixin):
    __tablename__ = "zonasconfiguracion"
    id = Column("idzonasconfiguracion", Integer, primary_key=True, autoincrement=True)
    name = Column("nombre", String(45))
    interval = Column("intervalo", String(45), comment='En minutos')
    schedule_zone_configuration_id = Column("idhorariozonaconfiguracion", Integer, ForeignKey('horariozonaconfiguracion.idhorariozonaconfiguracion'), index=True)

    schedule_zone_configuration = relationship("ScheduleZoneConfiguration")

class ScheduleZoneConfiguration(db.Model, SerializerMixin):
    __tablename__ = "horariozonaconfiguracion"

    idhorariozonaconfiguracion = Column(Integer, primary_key=True, autoincrement=True)
    dia = Column(String(45))
    horainicial = Column(String(45))
    horafinal = Column(String(45))



class ModuleMenu(db.Model, SerializerMixin):
    __tablename__ = "modulos_menu"

    id = Column("idmodulos_menu", Integer, primary_key=True, autoincrement=True)
    module_id = Column("idmodulos",Integer, ForeignKey('modulos.idmodulos'), index=True)
    menu = Column("menu", String(100))
    file = Column("archivo", String(100))
    file_path = Column("ubicacion_archivo", String(100))
    level = Column("nivel", Integer)
    status = Column("estatus", Integer)
    icon = Column("icono", String(45))
    admin = Column("admin", Integer)

    module = relationship("Module")

class Module(db.Model, SerializerMixin):
    __tablename__ = "modulos"

    id = Column("idmodulos", Integer, primary_key=True, autoincrement=True)
    name = Column("modulo", String(100))
    level = Column("nivel", Integer)
    status = Column("estatus", Integer)
    icon = Column("icono", String(45))
    admin = Column("admin", Integer)

class Permission(db.Model, SerializerMixin):
    __tablename__ = "perfiles_permisos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    profile_id = Column("idperfiles", Integer, ForeignKey('perfiles.idperfiles'), index=True)
    module_menu_id = Column("idmodulos_menu", Integer, ForeignKey('modulos_menu.idmodulos_menu'), index=True)
    insert = Column("insertar", Integer)
    delete = Column("borrar", Integer)
    edit = Column("modificar", Integer)
    admin = Column("admin", Integer, comment="1: En nuevo manager 0: Aun no disponible en el nuevo manager")

    profile = relationship("Profile")
    module_menu = relationship("ModuleMenu")

class Profile(db.Model, SerializerMixin):
    __tablename__ = "perfiles"

    id = Column("idperfiles", Integer, primary_key=True, autoincrement=True)
    name = Column("perfil", String(100))
    status = Column("estatus", Integer)

class UserType(db.Model, SerializerMixin):
    __tablename__ = "tipousuario"

    id = Column("idtipousuario", Integer, primary_key=True, autoincrement=True)
    name = Column("nombretipo", String(255))
    show_on_app = Column("mostrarenapp", Integer)
    status = Column("estatus", Integer)
    default = Column("predeterminado", Integer)
    access_system = Column("sistema", Integer)
    is_costumer = Column("cliente", Integer)

class UserEnterprise(db.Model, SerializerMixin):
    __tablename__ = "usuario_empresa"

    id = Column('idempresausuario',Integer, primary_key=True, autoincrement=True)
    user_id = Column('idusuario',Integer, ForeignKey('usuarios_central.idusuarios'), nullable=False)
    club_id = Column('idempresa',Integer, ForeignKey('empresa.idempresa'), nullable=False)
    user_type_id = Column('idtipousuario',Integer, ForeignKey('tipousuario.idtipousuario'), nullable=False)

    user = relationship("UsersCentral")
    club = relationship("Enterprise")
    user_type = relationship("UserType")

class UsuarioFavorito(db.Model, SerializerMixin):
    __tablename__ = 'usuario_favorito'

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    user_id = Column('idusuario',db.Integer, db.ForeignKey('usuarios_central.idusuarios'), nullable=False)
    club_id = Column('idempresa',db.Integer, db.ForeignKey('empresa.idempresa'), nullable=False)
    status = db.Column('estatus',db.SmallInteger, nullable=False, default=1) 

    user = db.relationship("UsersCentral")
    club = db.relationship("Enterprise")