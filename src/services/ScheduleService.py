from typing import Any, Union, Optional
from datetime import time

from flask import jsonify
from ..models.schedule import Schedule
from ..database.db import get_connection_servicecode_orm
from ..utils.Text import get_db_name_app
from ..utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class ScheduleService:

    @classmethod
    def get_schedule(cls, service_code: int) -> list:
        """
            Get a list of court information from 'zonas' table.

            Args:
                service_code (int): The service code for database connection.

            Returns:
                list: A list containing the courts information.

            Raises:
                CustomException: If an error occurs during the retrieval process or if the court is not found.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                schedule = db_session.query(Schedule).first()

                return schedule.to_dict()
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def update_schedule(cls, service_code: int, monday: Optional[int] = None, tuesday: Optional[int] = None,
                    wednesday: Optional[int] = None, thursday: Optional[int] = None, friday: Optional[int] = None,
                    saturday: Optional[int] = None, sunday: Optional[int] = None, holiday: Optional[int] = None,
                    monday_start: Optional[time] = None, tuesday_start: Optional[time] = None,
                    wednesday_start: Optional[time] = None, thursday_start: Optional[time] = None,
                    friday_start: Optional[time] = None, saturday_start: Optional[time] = None,
                    sunday_start: Optional[time] = None, holiday_start: Optional[time] = None,
                    monday_end: Optional[time] = None, tuesday_end: Optional[time] = None,
                    wednesday_end: Optional[time] = None, thursday_end: Optional[time] = None,
                    friday_end: Optional[time] = None, saturday_end: Optional[time] = None,
                    sunday_end: Optional[time] = None, holiday_end: Optional[time] = None, **kwars) -> dict:
        """
        Update schedule data information in the 'club_horario' table.
       
        Args:
        service_code (int): The service code for the database connection.
        monday (Optional[int]): The data for Monday (optional).
        tuesday (Optional[int]): The data for Tuesday (optional).
        wednesday (Optional[int]): The data for Wednesday (optional).
        thursday (Optional[int]): The data for Thursday (optional).
        friday (Optional[int]): The data for Friday (optional).
        saturday (Optional[int]): The data for Saturday (optional).
        sunday (Optional[int]): The data for Sunday (optional).
        holiday (Optional[int]): The data for holiday (optional).
        monday_start (Optional[datetime.time]): The start time for Monday (optional).
        tuesday_start (Optional[datetime.time]): The start time for Tuesday (optional).
        wednesday_start (Optional[datetime.time]): The start time for Wednesday (optional).
        thursday_start (Optional[datetime.time]): The start time for Thursday (optional).
        friday_start (Optional[datetime.time]): The start time for Friday (optional).
        saturday_start (Optional[datetime.time]): The start time for Saturday (optional).
        sunday_start (Optional[datetime.time]): The start time for Sunday (optional).
        holiday_start (Optional[datetime.time]): The start time for holiday (optional).
        monday_end (Optional[datetime.time]): The end time for Monday (optional).
        tuesday_end (Optional[datetime.time]): The end time for Tuesday (optional).
        wednesday_end (Optional[datetime.time]): The end time for Wednesday (optional).
        thursday_end (Optional[datetime.time]): The end time for Thursday (optional).
        friday_end (Optional[datetime.time]): The end time for Friday (optional).
        saturday_end (Optional[datetime.time]): The end time for Saturday (optional).
        sunday_end (Optional[datetime.time]): The end time for Sunday (optional).
        holiday_end (Optional[datetime.time]): The end time for holiday (optional).

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the update process.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:

                # enterprise_data : Union[Enterprise, Any] = Enterprise.query.filter(Enterprise.service_code == service_code).filter(Enterprise.status == 1).first()

                db_session: Session

                schedule: Union[Schedule, Any] = db_session.query(Schedule).first()

                if schedule is None:
                    raise MissingDataException(Schedule.__tablename__, engine.url.database)
                
                schedule.monday = monday if monday is not None else schedule.monday
                schedule.tuesday = tuesday if tuesday is not None else schedule.tuesday
                schedule.wednesday = wednesday if wednesday is not None else schedule.wednesday
                schedule.thursday = thursday if thursday is not None else schedule.thursday
                schedule.friday = friday if friday is not None else schedule.friday
                schedule.saturday = saturday if saturday is not None else schedule.saturday
                schedule.sunday = sunday if sunday is not None else schedule.sunday
                schedule.holiday = holiday if holiday is not None else schedule.holiday

                schedule.monday_start = monday_start if monday_start is not None else schedule.monday_start
                schedule.tuesday_start = tuesday_start if tuesday_start is not None else schedule.tuesday_start
                schedule.wednesday_start = wednesday_start if wednesday_start is not None else schedule.wednesday_start
                schedule.thursday_start = thursday_start if thursday_start is not None else schedule.thursday_start
                schedule.friday_start = friday_start if friday_start is not None else schedule.friday_start
                schedule.saturday_start = saturday_start if saturday_start is not None else schedule.saturday_start
                schedule.sunday_start = sunday_start if sunday_start is not None else schedule.sunday_start
                schedule.holiday_start = holiday_start if holiday_start is not None else schedule.holiday_start

                schedule.monday_end = monday_end if monday_end is not None else schedule.monday_end
                schedule.tuesday_end = tuesday_end if tuesday_end is not None else schedule.tuesday_end
                schedule.wednesday_end = wednesday_end if wednesday_end is not None else schedule.wednesday_end
                schedule.thursday_end = thursday_end if thursday_end is not None else schedule.thursday_end
                schedule.friday_end = friday_end if friday_end is not None else schedule.friday_end
                schedule.saturday_end = saturday_end if saturday_end is not None else schedule.saturday_end
                schedule.sunday_end = sunday_end if sunday_end is not None else schedule.sunday_end
                schedule.holiday_end = holiday_end if holiday_end is not None else schedule.holiday_end

                db_session.commit()
                    
                return schedule.to_dict()
            
        except CustomException as ex:
            print(f'ScheduleRoute.py - update_schedule() - Error: {str(ex)}')
            raise CustomException(ex)