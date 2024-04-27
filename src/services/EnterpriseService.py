from typing import Any, Union, Optional

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
        
            enterprise_data : Union[Enterprise, Any] = Enterprise.query.filter(Enterprise.service_code == service_code).filter(Enterprise.status == 1).first()

            response = enterprise_data.to_dict()

            return response
            
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def update_enterprise(cls, service_code: int, name: Optional[str] = None, cellphone: Optional[str] = None, 
        telephone: Optional[str] = None, latitude: Optional[str] = None, longitude: Optional[str] = None, postal_code: Optional[str] = None, 
        country: Optional[str] = None, city: Optional[str] = None,state: Optional[str] = None, settlement: Optional[str] = None, neighborhood: Optional[str] = None, 
        address: Optional[str] = None) -> dict:
        """
        Update enterprise data information in the 'empresas' table.

        Args:
            service_code (int): The service code for database connection.
            name (Optional[str]): The name of the enterprise (optional).
            address (Optional[str]): The address of the enterprise (optional).
            cellphone (Optional[str]) : the cellphone of the enterprise(optional).
            telephone (Optional[str]) : the telephone of the enterprise(optional).
            latitude (Optional[str]) : the latitude of the enterprise(optional).
            longitude (Optional[str]) : the longitude  of the enterprise(optional).
            postal_code (Optional[str]) : the postal_code of the enterprise(optional).
            country (Optional[str]) : the country of the enterprise(optional).
            city (Optional[str]) : the city of the enterprise(optional).
            state (Optional[str]) : the state of the enterprise(optional).
            settlement (Optional[str]) : the settlement of the enterprise(optional).
            neighborhood (Optional[str]) : the neighborhood of the enterprise(optional).
            address (Optional[str]) : the address of the enterprise(optional).

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the update process.
        """
        try:
            enterprise_data : Union[Enterprise, Any] = Enterprise.query.filter(Enterprise.service_code == service_code).filter(Enterprise.status == 1).first()

            if enterprise_data is None:
                raise MissingDataException(Enterprise.__tablename__, get_db_name_app(),)
            
            if name is not None and name.strip():
                enterprise_data.name = name

            if cellphone is not None and cellphone.strip():
                enterprise_data.cellphone = cellphone
            if telephone is not None and telephone.strip():
                enterprise_data.telephone = telephone

            if latitude is not None and latitude.strip():
                enterprise_data.latitude = latitude

            if longitude is not None and longitude.strip():
                enterprise_data.longitude = longitude
            if postal_code is not None and postal_code.strip():
                enterprise_data.postal_code = postal_code
                
            if country is not None and country.strip():
                enterprise_data.country = country
            
            if city is not None and city.strip():
                enterprise_data.city = city

            if state is not None and state.strip():
                enterprise_data.state = state
                
            if settlement is not None and settlement.strip():
                enterprise_data.settlement = settlement

            if neighborhood is not None and neighborhood.strip():
                enterprise_data.neighborhood = neighborhood
                
            if address is not None and address.strip():
                enterprise_data.address = address
                
            db.session.commit()

            return {'data': enterprise_data.to_dict() , 'success': True}
        
        except CustomException as ex:
            print(f'EnterpriseRoute.py - update_enterprise() - Error: {str(ex)}')
            raise CustomException(ex)