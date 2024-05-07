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
    def update_schedule(cls, service_code: int, monday_enabled: Optional[int] = None, tuesday_enabled: Optional[int] = None,
                    wednesday_enabled: Optional[int] = None, thursday_enabled: Optional[int] = None, friday_enabled: Optional[int] = None,
                    saturday_enabled: Optional[int] = None, sunday_enabled: Optional[int] = None, holiday_enabled: Optional[int] = None,
                    monday_start: Optional[time] = None, tuesday_start: Optional[time] = None,
                    wednesday_start: Optional[time] = None, thursday_start: Optional[time] = None,
                    friday_start: Optional[time] = None, saturday_start: Optional[time] = None,
                    sunday_start: Optional[time] = None, holiday_start: Optional[time] = None,
                    monday_finish: Optional[time] = None, tuesday_finish: Optional[time] = None,
                    wednesday_finish: Optional[time] = None, thursday_finish: Optional[time] = None,
                    friday_finish: Optional[time] = None, saturday_finish: Optional[time] = None,
                    sunday_finish: Optional[time] = None, holiday_finish: Optional[time] = None, **kwars) -> dict:
        """
        Update schedule data information in the 'club_horario' table.
       
        Args:
        service_code (int): The service code for the database connection.
        monday_enabled (Optional[int]): The data for Monday (optional).
        tuesday_enabled (Optional[int]): The data for Tuesday (optional).
        wednesday (Optional[int]): The data for Wednesday (optional).
        thursday_enabled (Optional[int]): The data for Thursday (optional).
        friday_enabled (Optional[int]): The data for Friday (optional).
        saturday_enabled (Optional[int]): The data for Saturday (optional).
        sunday_enabled (Optional[int]): The data for Sunday (optional).
        holiday_enabled (Optional[int]): The data for holiday (optional).
        monday_start (Optional[datetime.time]): The start time for Monday (optional).
        tuesday_start (Optional[datetime.time]): The start time for Tuesday (optional).
        wednesday_start (Optional[datetime.time]): The start time for Wednesday (optional).
        thursday_start (Optional[datetime.time]): The start time for Thursday (optional).
        friday_start (Optional[datetime.time]): The start time for Friday (optional).
        saturday_start (Optional[datetime.time]): The start time for Saturday (optional).
        sunday_start (Optional[datetime.time]): The start time for Sunday (optional).
        holiday_start (Optional[datetime.time]): The start time for holiday (optional).
        monday_finish (Optional[datetime.time]): The finish time for Monday (optional).
        tuesday_finish (Optional[datetime.time]): The finish time for Tuesday (optional).
        wednesday_finish (Optional[datetime.time]): The finish time for Wednesday (optional).
        thursday_finish (Optional[datetime.time]): The finish time for Thursday (optional).
        friday_finish (Optional[datetime.time]): The finish time for Friday (optional).
        saturday_finish (Optional[datetime.time]): The finish time for Saturday (optional).
        sunday_finish (Optional[datetime.time]): The finish time for Sunday (optional).
        holiday_finish (Optional[datetime.time]): The finish time for holiday (optional).

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
                
                schedule.monday_enabled = monday_enabled if monday_enabled is not None else schedule.monday_enabled
                schedule.tuesday_enabled = tuesday_enabled if tuesday_enabled is not None else schedule.tuesday_enabled
                schedule.wednesday_enabled = wednesday_enabled if wednesday_enabled is not None else schedule.wednesday_enabled
                schedule.thursday_enabled = thursday_enabled if thursday_enabled is not None else schedule.thursday_enabled
                schedule.friday_enabled = friday_enabled if friday_enabled is not None else schedule.friday_enabled
                schedule.saturday_enabled = saturday_enabled if saturday_enabled is not None else schedule.saturday_enabled
                schedule.sunday_enabled = sunday_enabled if sunday_enabled is not None else schedule.sunday_enabled
                schedule.holiday_enabled = holiday_enabled if holiday_enabled is not None else schedule.holiday_enabled

                schedule.monday_start = monday_start if monday_start is not None else schedule.monday_start
                schedule.tuesday_start = tuesday_start if tuesday_start is not None else schedule.tuesday_start
                schedule.wednesday_start = wednesday_start if wednesday_start is not None else schedule.wednesday_start
                schedule.thursday_start = thursday_start if thursday_start is not None else schedule.thursday_start
                schedule.friday_start = friday_start if friday_start is not None else schedule.friday_start
                schedule.saturday_start = saturday_start if saturday_start is not None else schedule.saturday_start
                schedule.sunday_start = sunday_start if sunday_start is not None else schedule.sunday_start
                schedule.holiday_start = holiday_start if holiday_start is not None else schedule.holiday_start

                schedule.monday_finish = monday_finish if monday_finish is not None else schedule.monday_finish
                schedule.tuesday_finish = tuesday_finish if tuesday_finish is not None else schedule.tuesday_finish
                schedule.wednesday_finish = wednesday_finish if wednesday_finish is not None else schedule.wednesday_finish
                schedule.thursday_finish = thursday_finish if thursday_finish is not None else schedule.thursday_finish
                schedule.friday_finish = friday_finish if friday_finish is not None else schedule.friday_finish
                schedule.saturday_finish = saturday_finish if saturday_finish is not None else schedule.saturday_finish
                schedule.sunday_finish = sunday_finish if sunday_finish is not None else schedule.sunday_finish
                schedule.holiday_finish = holiday_finish if holiday_finish is not None else schedule.holiday_finish

                db_session.commit()
                    
                return schedule.to_dict()
            
        except CustomException as ex:
            print(f'ScheduleRoute.py - update_schedule() - Error: {str(ex)}')
            raise CustomException(ex)