from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'club_horario'

    id = Column('idclub_schedule', Integer, primary_key=True, autoincrement=True)

    monday = Column('lunes_activado', Integer, nullable=True , server_default="NULL")
    tuesday = Column('martes_activado', Integer, nullable=True , server_default="NULL")
    wednesday = Column('miercoles_activado', Integer, nullable=True , server_default="NULL")
    thursday= Column('jueves_activado', Integer, nullable=True , server_default="NULL")
    friday = Column('viernes_activado', Integer, nullable=True , server_default="NULL")
    saturday = Column('sabado_activado', Integer, nullable=True , server_default="NULL")
    sunday = Column('domingo_activado', Integer, nullable=True , server_default="NULL")
    holiday = Column('festivo_activado', Integer, nullable=True , server_default="NULL")

    monday_start = Column('lunes_inicio', Time, nullable=True , server_default="NULL")
    tuesday_start = Column('martes_inicio', Time, nullable=True , server_default="NULL")
    wednesday_start = Column('miercoles_inicio', Time, nullable=True , server_default="NULL")
    thursday_start = Column('jueves_inicio', Time, nullable=True , server_default="NULL")
    friday_start = Column('viernes_inicio', Time, nullable=True , server_default="NULL")
    saturday_start = Column('sabado_inicio', Time, nullable=True , server_default="NULL")
    sunday_start = Column('domingo_inicio', Time, nullable=True , server_default="NULL")
    holiday_start = Column('festivo_inicio', Time, nullable=True , server_default="NULL")
        
    monday_end = Column('lunes_final', Time, nullable=True, server_default="NULL")
    tuesday_end = Column('martes_final', Time, nullable=True, server_default="NULL")
    wednesday_end = Column('miercoles_final', Time, nullable=True, server_default="NULL")
    thursday_end = Column('jueves_final', Time, nullable=True, server_default="NULL")
    friday_end = Column('viernes_final', Time, nullable=True, server_default="NULL")
    saturday_end = Column('sabado_final', Time, nullable=True, server_default="NULL")
    sunday_end = Column('domingo_final', Time, nullable=True, server_default="NULL")
    holiday_end = Column('festivo_final', Time, nullable=True, server_default="NULL")




