from typing import Optional, Union, Any
from orm_models import Courts, Sport
from src.database.db import get_connection_servicecode_orm # Databas
from src.utils.errors.CustomException import CustomException, MissingDataException # Errors
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class CourtService():
    @classmethod
    def get_courts(cls, service_code: int) -> list:
        """
            Get a list of court information from 'zonas' table.

            Args:
                service_code (int): The service code for database connection.

            Returns:
                dict: A dictionary containing the court information.

            Raises:
                CustomException: If an error occurs during the retrieval process or if the court is not found.
        """
        try:
            items = []
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session

                courts = db_session.query(Courts).all()

                items = [court.to_json(cls.get_sport_name(court.sport)) for court in courts]

                return items
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def get_court(cls, id: int, service_code: int) -> dict:
        """
        Get court information from 'zonas' table based on court ID.

        Args:
            id (int): The ID of the court.
            service_code (int): The service code for database connection.

        Returns:
            list: A list containing the court information in a dictionary.

        Raises:
            CustomException: If an error occurs during the retrieval process or if the court is not found.
        """
        try:
            # Establish database connection and create session
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session

                court: Union[Courts, None] = db_session.query(Courts).get(id)

                if court is None:
                    raise MissingDataException(Courts.__tablename__, engine.url.database, id)
                
                sport_name = cls.get_sport_name(court.sport)

                court_json = court.to_json(sport_name)

                

                

                return court_json
        except CustomException as ex:
            raise CustomException(ex)


    @classmethod
    def save_court(cls, service_code: int, name: str, address: str, active: int, enable_reservation_app: int, color: str, image: str, id_zone_size: int, id_sport: int, id_court_type: int, id_court_caracteristic: int) -> dict:
        """
            Save a new court into 'zonas' table.

            Args:
                service_code (int): The service code for database connection.
                name (str): The name of the court.
                address (str): The address of the court.
                active (int): The active status of the court.
                enable_reservation_app (int): The status of the court for reservation app.
                color (str): The color of the court.
                image (str): The image URL of the court.
                id_zone_size (int): The ID of the zone size.
                id_sport (int): The ID of the sport.
                id_court_type (int): The ID of the court type.
                id_court_caracteristic (int): The ID of the court characteristic.

            Returns:
                dict: A dictionary containing the newly created court data.

            Raises:
                CustomException: If an error occurs during the saving process.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session

                new_court = Courts(
                    name = name, 
                    address = address, 
                    active = active, 
                    enable_reservation_app = enable_reservation_app, 
                    color = color, 
                    image = image, 
                    size_id = id_zone_size, 
                    sport = id_sport, 
                    type_id = id_court_type, 
                    characteristic_id = id_court_caracteristic)
                
                db_session.add(new_court)
                db_session.commit()

                sport_name = cls.get_sport_name(new_court.sport) 
                
                return new_court.to_json(sport_name)
        except Exception as ex:
            print(f'CourtService.py - save_court() - Error: {str(ex)}')
            raise CustomException(ex)

    @classmethod
    def get_sport_name(cls, id_sport):
        sport = Sport.query.get(id_sport)

        if sport:
            sport_name = sport.name
        else:
            sport_name = ''
        return sport_name
        
    @classmethod
    def update_court(cls, court_id: int, service_code: int, name: Optional[str] = None, address: Optional[str] = None, 
        active: Optional[int] = None, enable_reservation_app: Optional[int] = None, color: Optional[str] = None, 
        image: Optional[str] = None, id_zone_size: Optional[int] = None, id_sport: Optional[int] = None, id_court_type: Optional[int] = None, 
        id_court_caracteristic: Optional[int] = None) -> dict:
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
                
                sport_name = cls.get_sport_name(court.sport)

                cls.update_court_attributes(name, address, active, enable_reservation_app, color, image, id_zone_size, id_sport, id_court_type, id_court_caracteristic, court)

                db_session.commit()

                return {'data': court.to_json(sport_name), 'success': True}
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def update_court_attributes(cls, name, address, active, enable_reservation_app, color, image, id_zone_size, id_sport, id_court_type, id_court_caracteristic, court):
        if name is not None and name.strip():
            court.name = name.strip()

        if address is not None and address.strip():
            court.address = address.strip()

        if active is not None:
            court.active = active

        if enable_reservation_app is not None:
            court.enable_reservation_app = enable_reservation_app

        if color is not None and color.strip():
            court.color = color.strip()

        if image is not None:
            court.image = image

        if id_zone_size is not None:
            court.size_id = id_zone_size

        if id_sport is not None:
            court.sport = id_sport

        if id_court_type is not None:
            court.type_id = id_court_type

        if id_court_caracteristic is not None:
            court.characteristic_id = id_court_caracteristic

    @classmethod
    def delete_court(cls, court_id: int, service_code: int) -> dict:
        """
        Delete court from 'zonas' table based on court_id.
        
        Args:
            court_id (int): The ID of the court to delete.
            service_code (int): The service code for database connection.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the deletion process.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session
            
                court = db_session.query(Courts).get(court_id)

                if court is None:
                    return {'message': 'La cancha no existe', 'success': True}
                
                db_session.delete(court)
                db_session.commit()

                return {'message': 'Cancha eliminada exitosamente', 'success': True}
        except CustomException as ex:
            raise CustomException(ex)



