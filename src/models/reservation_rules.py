from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Time
from sqlalchemy_serializer import SerializerMixin
from extensions import db

class ReservationRules(db.Model, SerializerMixin):
    __tablename__ = 'reglas_reservacion'
    id = Column(Integer, primary_key= True, index= True)
    cancelation_policy = Column('politica_cancelacion', Integer)
    anticipated_reservation_limit = Column('limite_reserva_anticipada' ,Integer)
    max_reservation_day = Column('maxima_reservaciones_al_dia', Integer)
    max_active_reservations = Column('maximas_reservaciones_activas', Integer)
    pending_payment_time_limit = Column('tiempo_limite_pago_pendiente', Integer, default=7200) #7200s = 2h
    results_close = Column('cierre_resultados', Integer, nullable=False, default=1200) #1200s = 20min
    validate_close = Column('validacion_resultados', Integer, nullable=False, default=86400) #84600 = 24h - tiempo limite de validacion de resultados
    commission_service_amount= Column('comisionserviciomonto', Float(10), server_default='0.00')
    commission_service_percentage = Column('comisionservicioporcentaje', Float(10), server_default='0.00')
    absorb_commission = Column('absorber_comision', Boolean, default=False)