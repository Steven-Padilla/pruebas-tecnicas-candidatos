from typing import Any, Union

from flask import jsonify
from src.models import Enterprise
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class EnterpriseService:

    @classmethod
    def get_enterprise_data(cls, service_code:int) -> list:
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
            response = {}
        
            enterprise_data = Enterprise.query.filter(Enterprise.service_code == service_code).filter(Enterprise.status == 1).first()

            response = enterprise_data.to_dict()

            return response
            
        except CustomException as ex:
            raise CustomException(ex)

        
    @classmethod
    def update_court(cls, court_id: int, service_code: int, name: Optional[str] = None, address: Optional[str] = None, 
        active: Optional[int] = None, enable_reservation_app: Optional[int] = None, color: Optional[str] = None, 
        image: Optional[str] = None, id_zone_size: Optional[int] = None, id_sport: Optional[int] = None, id_court_type: Optional[int] = None, 
        id_court_characteristics: Optional[int] = None) -> dict:
        """
        Update court information in the 'zonas' table.

        Args:
            court_id (int): The ID of the court.
            service_code (int): The service code for database connection.
            name (Optional[str]): The name of the court (optional).
            address (Optional[str]): The address of the court (optional).
            active (Optional[int]): The active status of the court (optional).
            enable_reservation_app (Optional[int]): The status of the court for reservation app (optional).
            color (Optional[str]): The color of the court (optional).
            image (Optional[str]): The image URL of the court (optional).
            id_zone_size (Optional[int]): The ID of the zone size (optional).
            id_sport (Optional[int]): The ID of the sport (optional).
            id_court_type (Optional[int]): The ID of the court type (optional).
            id_court_caracteristic (Optional[int]): The ID of the court characteristic (optional).

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the update process.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session

                court: Union[Courts, Any] = db_session.query(Courts).get(court_id)

                if court is None:
                    raise MissingDataException(Courts.__tablename__, engine.url.database, court_id)
                
                cls.update_court_attributes(name, address, active, enable_reservation_app, color, image, id_zone_size, id_sport, id_court_type, id_court_characteristics, court)

                if id_sport is None:
                    sport = cls.get_sport(court.sport)
                else:
                    sport = cls.get_sport(id_sport)
                    
                db_session.commit()

                return {'data': court.to_json(sport), 'success': True}
        except CustomException as ex:
            print(f'CourtRoutes.py - update_court() - Error: {str(ex)}')
            raise CustomException(ex)