from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'club_horario'

    idclub_schedule = Column('idclub_schedule', Integer, primary_key=True, autoincrement=True)

    monday_enabled = Column('lunes_activado', Integer, nullable=True , server_default="NULL")
    tuesday_enabled = Column('martes_activado', Integer, nullable=True , server_default="NULL")
    wednesday_enabled = Column('miercoles_activado', Integer, nullable=True , server_default="NULL")
    thursday_enabled = Column('jueves_activado', Integer, nullable=True , server_default="NULL")
    friday_enabled = Column('viernes_activado', Integer, nullable=True , server_default="NULL")
    saturday_enabled = Column('sabado_activado', Integer, nullable=True , server_default="NULL")
    sunday_enabled = Column('domingo_activado', Integer, nullable=True , server_default="NULL")
    holiday_enabled = Column('festivo_activado', Integer, nullable=True , server_default="NULL")

    monday_start = Column('lunes_inicio', Time, nullable=True , server_default="NULL")
    tuesday_start = Column('martes_inicio', Time, nullable=True , server_default="NULL")
    wednesday_start = Column('miercoles_inicio', Time, nullable=True , server_default="NULL")
    thursday_start = Column('jueves_inicio', Time, nullable=True , server_default="NULL")
    friday_start = Column('viernes_inicio', Time, nullable=True , server_default="NULL")
    saturday_start = Column('sabado_inicio', Time, nullable=True , server_default="NULL")
    sunday_start = Column('domingo_inicio', Time, nullable=True , server_default="NULL")
    holiday_start = Column('festivo_inicio', Time, nullable=True , server_default="NULL")
        
    monday_finish = Column('lunes_final', Time, nullable=True, server_default="NULL")
    tuesday_finish = Column('martes_final', Time, nullable=True, server_default="NULL")
    wednesday_finish = Column('miercoles_final', Time, nullable=True, server_default="NULL")
    thursday_finish = Column('jueves_final', Time, nullable=True, server_default="NULL")
    friday_finish = Column('viernes_final', Time, nullable=True, server_default="NULL")
    saturday_finish = Column('sabado_final', Time, nullable=True, server_default="NULL")
    sunday_finish = Column('domingo_final', Time, nullable=True, server_default="NULL")
    holiday_finish = Column('festivo_final', Time, nullable=True, server_default="NULL")




